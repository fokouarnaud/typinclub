from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.views.decorators.vary import vary_on_cookie
from .models import LocalizedText, Asset, ExternalLink, Offer, Preview, FAQ


@require_safe
@vary_on_cookie
def home(request):
    language = request.GET.get('lang', request.COOKIES.get('yemx-lang', 'fr'))
    if language not in ('fr', 'en'):
        language = 'fr'
    localized = list(LocalizedText.objects.all())
    texts = {text.key: getattr(text, language) for text in localized}
    response = render(request, 'showcase/home.html', {'texts': texts, 'language': language,
        'logo': Asset.objects.filter(key='logo').first(),
        'assets': {asset.key: asset for asset in Asset.objects.select_related('alt')},
        'translations': {lang: {text.key: getattr(text, lang) for text in localized} for lang in ('fr', 'en')},
        'links': {link.key: link for link in ExternalLink.objects.select_related('label')},
        'legal_links': ExternalLink.objects.filter(key__in=['mentions', 'privacy', 'terms', 'sales']).select_related('label'),
        'offers': Offer.objects.select_related('name', 'period', 'external_link').prefetch_related('benefits__text'),
        'previews': Preview.objects.select_related('asset__alt', 'caption'),
        'faqs': FAQ.objects.select_related('question', 'answer'),
        'problems': ['notebook', 'calc', 'debt'],
        'features': ['sales', 'stock', 'credits', 'offline', 'multi', 'pdf'],
        'steps': ['s1', 's2', 's3']})
    response['Content-Language'] = language
    # Only the public template uses this strict policy. Unfold has its own
    # inline scripts/styles, so applying it globally would break administration.
    response['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; font-src 'self'; connect-src 'self'; "
        "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
    )
    if request.GET.get('lang') in ('fr', 'en'):
        response.set_cookie('yemx-lang', language, max_age=365 * 24 * 60 * 60, samesite='Lax', secure=request.is_secure())
    return response
