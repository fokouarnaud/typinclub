"""Email second factor for every admin request, including direct POSTs."""
import logging
import secrets
from datetime import timedelta
from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .models import AdminOTPChallenge

logger = logging.getLogger(__name__)


def digest(value):
    return salted_hmac('yemx-admin-otp', str(value), algorithm='sha256').hexdigest()


def verified(request):
    return request.session.get('admin_otp_verified') == digest(
        f'{request.user.pk}:{request.user.get_session_auth_hash()}:{request.session.session_key}')


class AdminOTPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (settings.ADMIN_OTP_REQUIRED and request.path.startswith('/admin/')
                and request.path not in ('/admin/login/', '/admin/logout/', '/admin/otp/')
                and request.user.is_authenticated and not verified(request)):
            return redirect('admin_otp')
        return self.get_response(request)


class OTPForm(forms.Form):
    code = forms.RegexField(r'^[0-9]{6}$', label='Code de vérification', max_length=6,
                           widget=forms.TextInput(attrs={'inputmode': 'numeric', 'autocomplete': 'one-time-code', 'autofocus': True}))


def issue_code(request):
    now = timezone.now()
    if not request.user.email:
        return 'Impossible d’envoyer le code : aucune adresse email configurée pour ce compte.'
    with transaction.atomic():
        challenge, _ = AdminOTPChallenge.objects.get_or_create(user=request.user)
        if challenge.locked_until and challenge.locked_until > now:
            return 'Trop de tentatives. Réessayez dans dix minutes.'
        if challenge.sent_at and challenge.sent_at + timedelta(seconds=60) > now:
            return 'Patientez une minute avant de demander un autre code.'
        code = f'{secrets.randbelow(1000000):06d}'
        challenge.digest = digest(code)
        challenge.session_digest = digest(request.session.session_key)
        challenge.sent_at = now
        challenge.expires_at = now + timedelta(minutes=5)
        challenge.attempts = 0
        challenge.locked_until = None
        challenge.save()
    try:
        count = send_mail('YemX — Code de connexion administrateur',
                         f'Votre code de connexion YemX est {code}. Il expire dans 5 minutes. '
                         'Si vous n’avez pas demandé ce code, ignorez cet email.',
                         settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)
        if count != 1:
            raise OSError('Mail backend did not send the message')
    except (OSError, SMTPException):
        # Never log SMTP exceptions: they can contain credentials or message bodies.
        logger.warning('Admin OTP email delivery failed')
        AdminOTPChallenge.objects.filter(user=request.user, digest=digest(code)).update(digest='')
        return 'Impossible d’envoyer le code actuellement. Réessayez dans une minute.'
    return 'Un code a été envoyé à l’adresse email de votre compte.'


def accept_code(request, code):
    now = timezone.now()
    with transaction.atomic():
        challenge = AdminOTPChallenge.objects.filter(user=request.user).first()
        if not challenge or (challenge.locked_until and challenge.locked_until > now):
            return False
        challenge.attempts += 1
        valid = (bool(challenge.digest) and challenge.expires_at and challenge.expires_at > now
                 and constant_time_compare(challenge.session_digest, digest(request.session.session_key))
                 and constant_time_compare(challenge.digest, digest(code)))
        if valid:
            challenge.digest = ''
        elif challenge.attempts >= 5:
            challenge.locked_until = now + timedelta(minutes=10)
            challenge.digest = ''
        challenge.save()
    if valid:
        request.session.cycle_key()
        request.session['admin_otp_verified'] = digest(
            f'{request.user.pk}:{request.user.get_session_auth_hash()}:{request.session.session_key}')
    return bool(valid)


@never_cache
@csrf_protect
def otp_view(request):
    if not request.user.is_authenticated or not request.user.is_active or not request.user.is_staff:
        return redirect('/admin/login/?next=/admin/')
    if not settings.ADMIN_OTP_REQUIRED or verified(request):
        return redirect('/admin/')
    message = ''
    form = OTPForm(request.POST or None)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            logout(request)
            return redirect('/admin/login/')
        if 'resend' in request.POST:
            message = issue_code(request)
            form = OTPForm()
        elif form.is_valid():
            if accept_code(request, form.cleaned_data['code']):
                return redirect('/admin/')
            message = 'Code invalide, expiré ou trop de tentatives. Demandez un nouveau code si nécessaire.'
    else:
        challenge = AdminOTPChallenge.objects.filter(user=request.user).first()
        if not challenge or not challenge.expires_at or challenge.expires_at <= timezone.now():
            message = issue_code(request)
        else:
            message = 'Saisissez le code envoyé à l’adresse email de votre compte.'
    return render(request, 'showcase/admin_otp.html', {'form': form, 'message': message})
