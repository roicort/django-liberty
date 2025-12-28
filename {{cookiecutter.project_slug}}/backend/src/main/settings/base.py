from os import environ
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from django.utils.csp import CSP
from django.utils.translation import gettext_lazy as _

######################################################################
# General
######################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = str(environ.get("DEBUG", "true")).lower() in ("1", "true", "yes", "on")

SITE_URL = environ.get("DJANGO_URL", "http://localhost").strip()
FRONTEND_URL = environ.get("FRONTEND_URL", "http://localhost").strip()


def _clean_host(value):
    if not value:
        return ""
    return value.replace("http://", "").replace("https://", "").strip().strip("/")


ALLOWED_HOSTS = [
    host
    for host in [
        _clean_host(SITE_URL),
        _clean_host(FRONTEND_URL),
        *[_clean_host(host) for host in environ.get("ALLOWED_HOSTS", "").split(",")],
    ]
    if host
]

CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in [
        SITE_URL.strip().rstrip("/"),
        FRONTEND_URL.strip().rstrip("/"),
        *[
            origin.strip().rstrip("/")
            for origin in environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
        ],
    ]
    if origin
]

WSGI_APPLICATION = "main.wsgi.application"

ROOT_URLCONF = "main.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

######################################################################
# Security

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "img-src": [CSP.SELF, "https:"],
}

######################################################################
# Apps
######################################################################
INSTALLED_APPS = [
    # Unfold Admin
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    # Django Contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # DRF
    "rest_framework",
    "drf_spectacular",
    # Auth
    "account",
    "oidc_provider",
    # Main
    "main",
]

if DEBUG:
    INSTALLED_APPS += [
        "whitenoise.runserver_nostatic",
    ]

######################################################################
# Middleware
######################################################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

######################################################################
# Database
######################################################################
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": environ.get("DB_USER"),
        "PASSWORD": environ.get("DB_PASSWORD"),
        "NAME": environ.get("DB_NAME"),
        "HOST": environ.get("DB_HOST"),
        "PORT": environ.get("DB_PORT"),
        "TEST": {
            "NAME": "test",
        },
    }
}

######################################################################
# Authentication
######################################################################
AUTH_USER_MODEL = "account.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/account/login/"

OIDC_USERINFO = "main.settings.oidc.userinfo"

# OIDC_EXTRA_SCOPE_CLAIMS = 'main.settings.oidc.CustomScopeClaims'

######################################################################
# Internationalization
######################################################################
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

######################################################################
# Staticfiles
######################################################################

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

######################################################################
# Storages
######################################################################

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

######################################################################
# Rest Framework
######################################################################
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_HEADER": _("{{cookiecutter.project_name}}"),
    "SITE_TITLE": _("{{cookiecutter.project_name}} Admin"),
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:account_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "label",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}

######################################################################
# Print Settings
######################################################################

if DEBUG:
    print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
    print(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
    print(f"DJANGO_URL: {SITE_URL}")
    print(f"FRONTEND_URL: {FRONTEND_URL}")
    print(f"WSGI_APPLICATION: {WSGI_APPLICATION}")
    print(f"ROOT_URLCONF: {ROOT_URLCONF}")
    print(f"DEFAULT_AUTO_FIELD: {DEFAULT_AUTO_FIELD}")
    print(f"INSTALLED_APPS: {INSTALLED_APPS}")
    print(f"MIDDLEWARE: {MIDDLEWARE}")
    print(f"TEMPLATES: {TEMPLATES}")
    print(f"DATABASES: {DATABASES}")
    print(f"AUTH_USER_MODEL: {AUTH_USER_MODEL}")
    print(f"LOGIN_URL: {LOGIN_URL}")
    print(f"LANGUAGE_CODE: {LANGUAGE_CODE}")
    print(f"TIME_ZONE: {TIME_ZONE}")
    print(f"USE_I18N: {USE_I18N}")
    print(f"USE_TZ: {USE_TZ}")
    print(f"STATIC_ROOT: {STATIC_ROOT}")
    print(f"STATIC_URL: {STATIC_URL}")
    print(f"MEDIA_ROOT: {MEDIA_ROOT}")
