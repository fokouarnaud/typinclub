import pytest
from django.core.management import call_command, get_commands
from showcase.models import LocalizedText, Asset, Preview, FAQ, Offer, ExternalLink, OfferBenefit

pytestmark = pytest.mark.django_db


def test_seed_is_complete_reproducible_and_preserves_edits():
    assert 'seed_content' in get_commands(), 'A reproducible content loader is required'
    call_command('seed_content')
    assert Preview.objects.count() == 4
    assert Asset.objects.count() == 5
    assert FAQ.objects.count() == 6
    assert list(Offer.objects.values_list('price', flat=True)) == [0, 2500]
    assert ExternalLink.objects.count() == 9
    assert all(t.fr.strip() and t.en.strip() for t in LocalizedText.objects.all())
    text = LocalizedText.objects.get(key='hero.subtitle')
    text.fr = 'Contenu corrigé par un administrateur'
    text.save()
    faq = FAQ.objects.first()
    faq.order = 99
    faq.save()
    call_command('seed_content')
    text.refresh_from_db()
    faq.refresh_from_db()
    assert text.fr == 'Contenu corrigé par un administrateur'
    assert faq.order == 99
    assert FAQ.objects.count() == 6


def test_seed_preserves_changed_benefit_text_and_order():
    call_command('seed_content')
    benefit = OfferBenefit.objects.filter(offer__code='free').first()
    benefit.text = LocalizedText.objects.get(key='hero.subtitle')
    benefit.order = 99
    benefit.save()
    call_command('seed_content')
    benefit.refresh_from_db()
    assert OfferBenefit.objects.filter(offer__code='free').count() == 5
    assert benefit.text.key == 'hero.subtitle'
    assert benefit.order == 99
