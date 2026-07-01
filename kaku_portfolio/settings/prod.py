"""Production settings. Used by wsgi.py / asgi.py."""

from .base import *  # noqa: F401,F403

DEBUG = False

# Required in production — no default, so a missing env var fails loudly.
SECRET_KEY = env("SECRET_KEY")  # noqa: F405

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])  # noqa: F405

# Postgres via DATABASE_URL, e.g. postgres://user:pass@host:5432/dbname
DATABASES = {"default": env.db("DATABASE_URL")}  # noqa: F405

# Hashed, compressed static files served by WhiteNoise.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

# Security hardening (see plan §11).
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Email backend is left to deploy-time env wiring (SMTP / provider).
