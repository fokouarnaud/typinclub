"""PythonAnywhere-only settings: its managed proxy supplies the HTTPS header."""
from .settings import *  # noqa: F403
from django.core.exceptions import ImproperlyConfigured

if DEBUG:  # noqa: F405
    raise ImproperlyConfigured('Production requires DJANGO_DEBUG=0.')
if not ADMIN_OTP_REQUIRED:  # noqa: F405
    raise ImproperlyConfigured('Production requires administrator email OTP.')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
