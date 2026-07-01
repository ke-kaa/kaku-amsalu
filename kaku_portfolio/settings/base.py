"""
Base settings shared by all environments.

Environment-specific overrides live in dev.py / prod.py, which import
everything from here with `from .base import *`.
"""

from pathlib import Path

import environ

# settings/base.py is two levels below the project root (which holds manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")  # no-op if the file is absent


# SECURITY ---------------------------------------------------------------------
# Dev-friendly default; prod.py re-reads this with no default so it is required.
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-o)(@im-5n^(t^xj33e@))wsi7n+q&1p#*e1=r2qgd3kx=99xdu",
)
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# APPLICATIONS -----------------------------------------------------------------
INSTALLED_APPS = [
    # admin_interface + colorfield MUST precede django.contrib.admin
    "admin_interface",
    "colorfield",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Third-party
    "solo",
    "tinymce",
    "imagekit",
    "ordered_model",
    "corsheaders",
    "rest_framework",

    # Local
    "apps.core",
    "apps.services",
    "apps.resume",
    "apps.skills",
    "apps.projects",
    "apps.api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kaku_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_globals",
            ],
        },
    },
]

WSGI_APPLICATION = "kaku_portfolio.wsgi.application"


# DATABASE ---------------------------------------------------------------------
# sqlite by default; prod.py overrides with Postgres from DATABASE_URL.
database_url = env("DATABASE_URL")
if database_url:
    try:
        DATABASES = {
            "default": env.db()
        }
    except Exception:
        DATABASES = {
            "deafult": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            "CONN_MAX_AGE": 600,
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            "CONN_MAX_AGE": 600,
        }
    }

# PASSWORD VALIDATION ----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# I18N -------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# STATIC & MEDIA ---------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# DEFAULTS ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-admin-interface requirements
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# EMAIL ------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@kakuportfolio.local")
CONTACT_EMAIL = env("CONTACT_EMAIL", default="amsalukaku122@gmail.com")
