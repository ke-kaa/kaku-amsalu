"""Development settings. Default for manage.py."""

from .base import *  # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Print emails to the console instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Inherits the sqlite DATABASES from base.py.
