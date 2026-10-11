import re
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core import mail
from django.test import Client, override_settings
from django.utils import timezone

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def otp_settings(settings):
    settings.ADMIN_OTP_REQUIRED = True
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


def password_login(client, user):
    user.email = 'admin@example.com'
    if not user.check_password('test-password-968!'):
        user.set_password('test-password-968!')
    user.save()
    return client.post('/admin/login/', {'username': user.username, 'password': 'test-password-968!'})


def get_code(client):
    response = client.get('/admin/otp/')
    assert response.status_code == 200
    return re.search(r'\b\d{6}\b', mail.outbox[-1].body).group()


def test_password_alone_cannot_read_or_write_admin(client, admin_user, seeded):
    password_login(client, admin_user)
    assert client.get('/admin/')['Location'] == '/admin/otp/'
    assert client.post('/admin/showcase/localizedtext/1/change/', {'fr': 'changed'})['Location'] == '/admin/otp/'
    code = get_code(client)
    assert mail.outbox[-1].to == ['admin@example.com']
    assert client.post('/admin/otp/', {'code': code})['Location'] == '/admin/'
    assert client.get('/admin/').status_code == 200
    assert client.post('/admin/otp/', {'code': code}).status_code == 302
    client.post('/admin/logout/')
    password_login(client, admin_user)
    assert client.get('/admin/')['Location'] == '/admin/otp/'
    assert client.post('/admin/otp/', {'code': code}).status_code == 200


def test_codes_are_session_bound_and_expire(client, admin_user):
    password_login(client, admin_user)
    code = get_code(client)
    other = Client()
    password_login(other, admin_user)
    assert other.post('/admin/otp/', {'code': code}).status_code == 200
    assert other.get('/admin/')['Location'] == '/admin/otp/'
    with patch('showcase.otp.timezone.now', return_value=timezone.now() + timedelta(minutes=6)):
        assert client.post('/admin/otp/', {'code': code}).status_code == 200
    assert client.get('/admin/')['Location'] == '/admin/otp/'


def test_attempt_limit_and_resend_cooldown_survive_new_sessions(client, admin_user):
    password_login(client, admin_user)
    code = get_code(client)
    wrong = '000000' if code != '000000' else '111111'
    for _ in range(5):
        assert client.post('/admin/otp/', {'code': wrong}).status_code == 200
    assert client.post('/admin/otp/', {'code': code}).status_code == 200
    other = Client()
    password_login(other, admin_user)
    other.get('/admin/otp/')
    assert len(mail.outbox) == 1
    assert other.get('/admin/')['Location'] == '/admin/otp/'


def test_no_mail_flood_csrf_or_anonymous_access(client, admin_user):
    assert client.get('/admin/otp/').status_code == 302
    password_login(client, admin_user)
    get_code(client)
    for _ in range(3):
        client.get('/admin/otp/')
        client.post('/admin/otp/', {'resend': '1'})
    assert len(mail.outbox) == 1
    csrf_client = Client(enforce_csrf_checks=True)
    csrf_client.force_login(admin_user)
    assert csrf_client.post('/admin/otp/', {'code': '123456'}).status_code == 403


def test_mail_failure_does_not_grant_access(client, admin_user):
    password_login(client, admin_user)
    with patch('showcase.otp.send_mail', side_effect=OSError('SMTP unavailable')):
        response = client.get('/admin/otp/')
    assert response.status_code == 200
    assert b'Impossible' in response.content
    assert client.get('/admin/')['Location'] == '/admin/otp/'


def test_empty_recipient_does_not_grant_access(client, admin_user):
    password_login(client, admin_user)
    admin_user.email = ''
    admin_user.save()
    response = client.get('/admin/otp/')
    assert response.status_code == 200
    assert len(mail.outbox) == 0
    assert client.get('/admin/')['Location'] == '/admin/otp/'
