"""Local adversarial requests only; pytest uses an isolated SQLite database."""
import json
import os
import subprocess
import sys
from datetime import timedelta

import pytest
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.test import Client, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.sessions.models import Session

from showcase.models import Asset, ExternalLink, LocalizedText

pytestmark = pytest.mark.django_db
PASSWORD = 'Only-for-isolated-tests-926!'


def production_config(**changes):
    env = dict(os.environ, DJANGO_DEBUG='0',
               DJANGO_SECRET_KEY='test-only-configuration-key-' + 'aB9!x7' * 10,
               DJANGO_ALLOWED_HOSTS='testserver')
    for key, value in changes.items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    names = ['DEBUG', 'ALLOWED_HOSTS', 'SECRET_KEY', 'SESSION_COOKIE_SECURE',
             'CSRF_COOKIE_SECURE', 'SESSION_COOKIE_HTTPONLY', 'SESSION_COOKIE_SAMESITE',
             'SECURE_SSL_REDIRECT', 'SECURE_HSTS_SECONDS', 'SECURE_HSTS_INCLUDE_SUBDOMAINS',
             'SECURE_HSTS_PRELOAD', 'SECURE_PROXY_SSL_HEADER', 'SESSION_COOKIE_AGE']
    # Never print the key, including the synthetic one.
    code = ('import json; from django.conf import settings; '
            'print(json.dumps({k:getattr(settings,k) for k in ' + repr(names)
            + " if k != 'SECRET_KEY'}))")
    env['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    return subprocess.run([sys.executable, '-c', code], env=env, capture_output=True, text=True)


@pytest.fixture
def production():
    result = production_config()
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize('changes', [
    {'DJANGO_SECRET_KEY': ''}, {'DJANGO_SECRET_KEY': 'weak'},
    {'DJANGO_ALLOWED_HOSTS': ''}, {'DJANGO_ALLOWED_HOSTS': '*'},
    {'DJANGO_ALLOWED_HOSTS': 'testserver,*'}, {'DJANGO_DEBUG': 'typo'},
    {'DJANGO_DEBUG': None, 'DJANGO_SECRET_KEY': ''},
])
def test_unsafe_production_configuration_refuses_start(changes):
    result = production_config(**changes)
    assert result.returncode != 0, 'Unsafe configuration must fail closed'
    assert 'ImproperlyConfigured' in result.stderr


def test_production_https_cookies_and_transport(production, seeded, admin_user):
    admin_user.set_password(PASSWORD)
    admin_user.save()
    with override_settings(**production):
        client = Client(enforce_csrf_checks=True)
        redirect = client.get('/admin/login/')
        assert redirect.status_code == 301
        assert redirect['Location'] == 'https://testserver/admin/login/'
        # Forged proxy headers must not suppress the redirect.
        assert client.get('/admin/login/', HTTP_X_FORWARDED_PROTO='https').status_code == 301
        login = client.get('/admin/login/', secure=True)
        assert login.cookies['csrftoken']['secure']
        token = BeautifulSoup(login.content, 'html.parser').select_one('[name=csrfmiddlewaretoken]')['value']
        response = client.post('/admin/login/', {
            'username': admin_user.username, 'password': PASSWORD,
            'csrfmiddlewaretoken': token, 'next': '/admin/'}, secure=True,
            HTTP_ORIGIN='https://testserver')
        assert response.status_code == 302
        cookie = response.cookies['sessionid']
        assert cookie['secure'] and cookie['httponly']
        assert cookie['samesite'] == 'Lax'
        assert int(cookie['max-age']) == 28800
        assert response['Strict-Transport-Security'] == 'max-age=31536000'
        assert client.get('/?lang=en', secure=True).cookies['yemx-lang']['secure']


def test_public_csp_allows_local_assets_but_blocks_active_injection(client, seeded):
    response = client.get('/')
    policy = response['Content-Security-Policy']
    assert "script-src 'self'" in policy
    assert "object-src 'none'" in policy
    assert "base-uri 'none'" in policy
    assert "frame-ancestors 'none'" in policy
    assert 'unsafe-inline' not in policy and 'unsafe-eval' not in policy
    assert response['X-Content-Type-Options'] == 'nosniff'
    assert response['X-Frame-Options'] == 'DENY'


@pytest.mark.parametrize('language', ['fr', 'en'])
def test_stored_xss_in_text_attributes_and_translation_json(client, seeded, language):
    payload = '</script><script id="injected">alert(1)</script><img src=x onerror=alert(2)>"\' onmouseover="alert(3)'
    # Hit text nodes, attributes, FAQ, captions, pricing, and accessibility labels.
    LocalizedText.objects.all().update(fr=payload, en=payload)
    response = client.get('/', {'lang': language})
    html = BeautifulSoup(response.content, 'html.parser')
    assert html.select('#injected, img[onerror], [onmouseover]') == []
    assert len(html.select('script')) == 2  # local application JS and inert JSON
    assert payload in html.get_text()
    translations = json.loads(html.select_one('#editorial-translations').string)
    assert translations[language]['hero.subtitle'] == payload
    assert html.select_one('meta[name=description]')['content'] == payload


@pytest.mark.parametrize('payload', ["' OR 1=1 --", "'; DROP TABLE showcase_localizedtext; --", '<svg onload=alert(1)>'])
def test_query_cookie_and_admin_search_injection(client, admin_client, seeded, payload):
    before = LocalizedText.objects.count()
    client.cookies['yemx-lang'] = payload
    response = client.get('/', {'lang': payload})
    assert response.status_code == 200 and response['Content-Language'] == 'fr'
    assert payload.encode() not in response.content
    response = admin_client.get(reverse('admin:showcase_localizedtext_changelist'), {'q': payload})
    assert response.status_code == 200
    assert response.context['cl'].result_count == 0
    assert LocalizedText.objects.count() == before


def test_sql_login_payload_cannot_bypass_authentication(client, admin_user):
    response = client.post('/admin/login/', {'username': "' OR 1=1 --", 'password': PASSWORD})
    assert response.status_code == 200
    assert '_auth_user_id' not in client.session
    assert client.get('/admin/').status_code == 302


@pytest.mark.parametrize('url', ['javascript:alert(1)', 'data:text/html,<script>alert(1)</script>',
    '//evil.example/', 'https://user:pass@evil.example/', 'https://example.com/" onmouseover="alert(1)'])
def test_admin_rejects_active_url_payloads(admin_client, seeded, url):
    link = ExternalLink.objects.get(key='apk')
    original = link.url
    response = admin_client.post(reverse('admin:showcase_externallink_change', args=[link.pk]),
        {'url': url, 'label': link.label_id})
    assert response.status_code == 200
    assert response.context['adminform'].form.errors
    link.refresh_from_db()
    assert link.url == original


@pytest.mark.parametrize('path', ['../../config/settings.py', 'showcase/assets/../../../db.sqlite3',
    'C:/Windows/win.ini', 'showcase/assets/..\\..\\models.py'])
def test_asset_traversal_rejected(seeded, path):
    asset = Asset.objects.get(key='logo')
    asset.path = path
    with pytest.raises(ValidationError):
        asset.save()


def test_csrf_origin_forgery_cannot_modify_editorial_content(admin_user, seeded):
    client = Client(enforce_csrf_checks=True)
    client.force_login(admin_user)
    text = LocalizedText.objects.get(key='hero.subtitle')
    original = text.fr
    url = reverse('admin:showcase_localizedtext_change', args=[text.pk])
    form = client.get(url, secure=True)
    token = BeautifulSoup(form.content, 'html.parser').select_one('[name=csrfmiddlewaretoken]')['value']
    for data, origin in [({'fr': 'pwned', 'en': 'pwned'}, 'https://testserver'),
                         ({'fr': 'pwned', 'en': 'pwned', 'csrfmiddlewaretoken': token}, 'https://evil.example')]:
        assert client.post(url, data, secure=True, HTTP_ORIGIN=origin).status_code == 403
        text.refresh_from_db()
        assert text.fr == original


def test_session_fixation_logout_and_expiry(client, admin_user):
    admin_user.set_password(PASSWORD)
    admin_user.save()
    session = client.session
    session['prelogin'] = 'attacker-known-session'
    session.save()
    client.cookies['sessionid'] = session.session_key
    old_key = session.session_key
    response = client.post('/admin/login/', {'username': admin_user.username,
        'password': PASSWORD, 'next': 'https://evil.example/'})
    assert response.status_code == 302 and response['Location'] == '/admin/'
    authenticated_key = client.cookies['sessionid'].value
    assert authenticated_key != old_key
    replay = Client()
    replay.cookies['sessionid'] = old_key
    assert replay.get('/admin/').status_code == 302
    assert client.get('/admin/').status_code == 200
    assert client.post('/admin/logout/').status_code == 200
    replay.cookies['sessionid'] = authenticated_key
    assert replay.get('/admin/').status_code == 302
    client.force_login(admin_user)
    expired_key = client.cookies['sessionid'].value
    Session.objects.filter(session_key=expired_key).update(expire_date=timezone.now() - timedelta(seconds=1))
    assert client.get('/admin/').status_code == 302


def test_host_header_poisoning_rejected(client):
    with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver']):
        assert client.get('/', HTTP_HOST='evil.example').status_code == 400
        assert client.get('/admin/login/', HTTP_HOST='evil.example').status_code == 400


def test_stored_xss_is_inert_in_unfold(admin_client, seeded):
    text = LocalizedText.objects.get(key='hero.subtitle')
    payload = '<script id="injected">alert(1)</script><img src=x onerror=alert(2)>'
    text.fr = text.en = payload
    text.save()
    # The seeded catalog is paginated; explicitly select the attacked row.
    for url in (reverse('admin:showcase_localizedtext_changelist') + '?q=hero.subtitle',
                reverse('admin:showcase_localizedtext_change', args=[text.pk])):
        response = admin_client.get(url)
        assert response.status_code == 200
        html = BeautifulSoup(response.content, 'html.parser')
        assert html.select('#injected, img[onerror]') == []
        assert payload in html.get_text()


def test_login_csrf_and_forged_session_rejected(admin_user):
    client = Client(enforce_csrf_checks=True)
    assert client.post('/admin/login/', {'username': admin_user.username,
        'password': PASSWORD}).status_code == 403
    client.cookies['sessionid'] = 'forged-session-attacker-value'
    assert client.get('/admin/').status_code == 302
    assert '_auth_user_id' not in client.session
