from os import environ
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

######################################################################
# General
######################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = environ.get("DEBUG", False)

SITE_URL = environ.get("SITE_URL", "http://localhost").strip()
FRONTEND_URL = environ.get("FRONTEND_URL", "http://localhost").strip()

ALLOWED_HOSTS = [
    SITE_URL.replace("http://", "").replace("https://", ""),
    FRONTEND_URL.replace("http://", "").replace("https://", ""),
] + environ.get("ALLOWED_HOSTS", "").replace("http://", "").replace("https://", "").split(",")

WSGI_APPLICATION = "main.wsgi.application"

ROOT_URLCONF = "main.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

######################################################################
# Security

CSRF_TRUSTED_ORIGINS = [
    SITE_URL,
    FRONTEND_URL,
]

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
    # "unfold.contrib.guardian",  # optional, if django-guardian package is used
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
    "SITE_HEADER": _("django-liberty"),
    "SITE_TITLE": _("django-liberty Admin"),
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

print(f"DEBUG: {DEBUG}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
print(f"SITE_URL: {SITE_URL}")
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
