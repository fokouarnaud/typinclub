import pytest
from django.apps import apps
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


def test_localized_text_rejects_missing_translation_on_save():
    model = apps.get_model('showcase', 'LocalizedText', require_ready=True) if apps.all_models['showcase'] else None
    assert model is not None, 'The editorial text model must exist'
    with pytest.raises(ValidationError):
        model.objects.create(key='hero.title', fr='YemX', en='   ')


def test_editorial_entities_and_price_validation():
    from showcase import models
    assert hasattr(models, 'Offer'), 'Pricing must be backed by editorial models'
    text = models.LocalizedText.objects.create(key='name', fr='Pro', en='Pro')
    with pytest.raises(ValidationError):
        models.Offer.objects.create(code='pro', name=text, period=text, price=-1, order=0)
    link = models.ExternalLink.objects.create(key='pro', label=text, url='https://wa.me/237694208641')
    offer = models.Offer.objects.create(code='pro', name=text, period=text, price=2500, order=0, external_link=link)
    models.OfferBenefit.objects.create(offer=offer, text=text, order=0)
    with pytest.raises(ValidationError):
        models.OfferBenefit.objects.create(offer=offer, text=text, order=0)
    assert offer.cta_url == 'https://wa.me/237694208641'
    with pytest.raises(ValidationError):
        models.Offer.objects.create(code='other', name=text, period=text, price=0, order=1, cta_anchor='https://bad.example')


@pytest.mark.parametrize('url', ['http://example.com', '/apk/a.apk', 'javascript:alert(1)', 'https://user:password@example.com'])
def test_external_link_rejects_unsafe_or_relative_url(url):
    from showcase import models
    assert hasattr(models, 'ExternalLink'), 'External destinations must be validated'
    text = models.LocalizedText.objects.create(key='label', fr='Lien', en='Link')
    with pytest.raises(ValidationError):
        models.ExternalLink.objects.create(key='bad', label=text, url=url)


@pytest.mark.parametrize('path', ['../secret.txt', '/logo.webp', 'https://example.com/a.webp', 'missing.webp'])
def test_asset_rejects_paths_outside_supplied_assets(path):
    from showcase import models
    assert hasattr(models, 'Asset'), 'Assets must be limited to supplied static files'
    text = models.LocalizedText.objects.create(key='alt', fr='Logo', en='Logo')
    with pytest.raises(ValidationError):
        models.Asset.objects.create(key='bad', alt=text, path=path, source_url='https://yemxapp.com/logo.webp')
