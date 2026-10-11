import json
import os
import subprocess
import sys

import pytest


def run_config(**overrides):
    env = dict(os.environ, DJANGO_SETTINGS_MODULE='config.production', DJANGO_DEBUG='0',
               DJANGO_SECRET_KEY='test-only-' + 'A7!qZ3xB' * 10,
               DJANGO_ALLOWED_HOSTS='typinclub.pythonanywhere.com', DJANGO_ADMIN_OTP_REQUIRED='1')
    env.update(overrides)
    return subprocess.run([sys.executable, '-c',
        'import json; from django.conf import settings; '
        'print(json.dumps([settings.SECURE_PROXY_SSL_HEADER, settings.ADMIN_OTP_REQUIRED]))'],
        env=env, capture_output=True, text=True)


def test_pythonanywhere_configuration_trusts_managed_https_proxy():
    result = run_config()
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == [['HTTP_X_FORWARDED_PROTO', 'https'], True]


@pytest.mark.parametrize('changes', [{'DJANGO_DEBUG': '1'}, {'DJANGO_ADMIN_OTP_REQUIRED': '0'}])
def test_production_cannot_disable_debug_or_second_factor(changes):
    result = run_config(**changes)
    assert result.returncode != 0
    assert 'ImproperlyConfigured' in result.stderr
