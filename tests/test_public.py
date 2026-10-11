import pytest
from bs4 import BeautifulSoup
from showcase.models import LocalizedText

pytestmark = pytest.mark.django_db


def page(client, url='/'):
    response = client.get(url)
    assert response.status_code == 200
    return BeautifulSoup(response.content, 'html.parser')


def test_us01_public_editorial_content_and_section_order(client, seeded):
    response = client.get('/')
    assert response.status_code == 200
    html = BeautifulSoup(response.content, 'html.parser')
    assert [s['id'] for s in html.select('main > section')] == [
        'intro', 'problems', 'features', 'app-preview', 'how-it-works', 'pricing', 'stats', 'faq', 'download', 'about']
    assert 'Le cahier numérique' in html.h1.get_text()
    assert 'Ventes rapides' in html.select_one('#features').get_text()
    text = LocalizedText.objects.get(key='hero.subtitle')
    text.fr = '<script>alert("bad")</script>'
    text.save()
    response = client.get('/')
    assert b'<script>alert("bad")</script>' not in response.content
    assert b'&lt;script&gt;' in response.content


def test_public_route_does_not_accept_mutation(client):
    assert client.post('/', {'fr': 'overwrite'}).status_code == 405


def test_us02_downloads_use_real_absolute_destinations(client, seeded):
    html = page(client)
    assert html.select_one('#download a[data-link="play"]')['href'] == 'https://play.google.com/store/apps/details?id=com.yemxapp.app'
    assert html.select_one('#download a[data-link="apk"]')['href'] == 'https://yemxapp.com/apk/yemx-latest.apk'
    assert html.select_one('#download a[data-link="apk-older"]')['href'] == 'https://yemxapp.com/apk/yemx-latest.apk'
    assert html.select_one('[data-store="apple"]').name == 'span'
    assert html.select_one('a[data-link="pdf"]')['href'] == 'https://yemxapp.com/docs/exemple-rapport.pdf'
    assert len(html.select('footer a[data-legal]')) == 4
    assert all(a['href'].startswith('https://yemxapp.com/') for a in html.select('footer a[data-legal]'))


def test_us03_compare_prices_limits_and_contact_without_sending(client, seeded):
    html = page(client)
    offers = html.select('#pricing article')
    assert len(offers) == 2
    assert '0 FCFA' in offers[0].get_text()
    assert '2500 FCFA' in offers[1].get_text()
    assert '25 produits' in offers[0].get_text()
    assert 'illimités' in offers[1].get_text()
    assert offers[0].a['href'] == '#download'
    assert offers[1].a['href'] == 'https://wa.me/237694208641?text=Bonjour%2C%20je%20suis%20int%C3%A9ress%C3%A9(e)%20par%20l%27offre%20Pro%20de%20YemX.'


def test_us05_gallery_renders_ordered_local_assets_and_captions(client, seeded):
    from showcase.models import Preview
    preview = Preview.objects.get(key='dashboard')
    preview.order = 99
    preview.save()
    html = page(client)
    images = html.select('#app-preview img')
    assert len(images) == 4
    assert images[0]['src'] == '/static/showcase/assets/stock.webp'
    assert images[-1]['alt'] == 'Tableau de bord'
    assert html.select_one('#app-preview figcaption').get_text() == 'Gestion du stock'


def test_us06_faq_renders_six_ordered_questions_and_answers(client, seeded):
    html = page(client)
    questions = html.select('#faq details')
    assert len(questions) == 6
    assert "C'est vraiment gratuit ?" in questions[0].summary.get_text()
    assert '25 produits' in questions[0].p.get_text()
    assert not any(q.has_attr('open') for q in questions)


def test_us07_language_selection_persists_without_changing_destinations(client, seeded):
    html = page(client, '/?lang=en')
    assert html.html['lang'] == 'en'
    assert 'The digital ledger' in html.h1.get_text()
    assert 'Is it really free?' in html.select_one('#faq').get_text()
    assert 'Free' in html.select_one('#pricing').get_text()
    assert page(client).html['lang'] == 'en'
    assert html.select_one('[data-link="apk"]')['href'] == 'https://yemxapp.com/apk/yemx-latest.apk'
    assert page(client, '/?lang=fr').html['lang'] == 'fr'


def test_invalid_language_falls_back_to_french(client, seeded):
    client.cookies['yemx-lang'] = 'xx'
    assert page(client, '/?lang=xx').html['lang'] == 'fr'


def test_us04_us08_semantic_navigation_links_resolve_to_public_sections(client, seeded):
    html = page(client)
    navigation = html.select_one('#navbar nav')
    assert navigation is not None, 'The backend must provide semantic navigation'
    assert [a['href'] for a in navigation.select('a')] == ['#features', '#how-it-works', '#pricing', '#faq', '#download']
    assert html.select_one('a[href="#main"]') is not None
    for link in html.select('a[href^="#"]'):
        assert html.select_one(link['href']) is not None
    assert html.select_one('a[lang="en"]')['href'] == '?lang=en'
