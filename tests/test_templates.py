import pytest
from bs4 import BeautifulSoup
from django.contrib.staticfiles import finders

pytestmark = pytest.mark.django_db


def test_page_has_local_static_assets_and_interaction_controls(client, seeded):
    html = BeautifulSoup(client.get('/').content, 'html.parser')
    assert html.select_one('#menu-toggle') is not None
    assert html.select_one('#mobile-menu')['hidden'] == ''
    assert html.select_one('#preview-modal').name == 'dialog'
    assert len(html.select('#app-preview button[data-preview-index]')) == 4
    assert html.select_one('#preview-modal-close') is not None
    for asset in html.select('script[src], link[rel="stylesheet"], img[src]'):
        path = asset.get('src', asset.get('href'))
        assert path.startswith('/static/')
        assert finders.find(path.removeprefix('/static/')), path


def test_localized_accessible_labels_and_safe_translation_payload(client, seeded):
    from showcase.models import LocalizedText
    text = LocalizedText.objects.get(key='hero.subtitle')
    text.en = '</script><script>alert(1)</script>'
    text.save()
    html = BeautifulSoup(client.get('/?lang=en').content, 'html.parser')
    assert html.select_one('#menu-toggle')['aria-label'] == 'Open menu'
    assert html.select_one('#preview-modal-close')['aria-label'] == 'Close gallery'
    assert '</script>' not in html.select_one('#editorial-translations').get_text()
    assert all(svg.get('aria-hidden') == 'true' for svg in html.select('svg.icon'))


def test_about_mission_and_home_accessible_label_are_localized(client, seeded):
    html = BeautifulSoup(client.get('/?lang=en').content, 'html.parser')
    assert 'Our goal is to digitize' in html.select_one('#about').get_text()
    assert html.select_one('#navbar > a')['aria-label'] == 'YemX - Home'
