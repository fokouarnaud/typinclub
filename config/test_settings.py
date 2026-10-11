"""Explicit local settings for pytest, whose database is isolated by pytest-django."""
import os

os.environ.setdefault('DJANGO_DEBUG', '1')

from .settings import *  # noqa: F403
