import os
from pathlib import Path
from urllib.parse import urlsplit

from corsheaders.defaults import default_headers
from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from django.utils.csp import CSP
from django.utils.translation import gettext_lazy as _

######################################################################
# Utils
######################################################################


def _clean_host(value):
    """Returns just the host portion (no scheme, no port).

    Django's ALLOWED_HOSTS expects hostnames only, so we strip scheme and port.
    """

    if not value:
        return ""

    # urlsplit handles host/port cleanly even if scheme is missing.
    parsed = urlsplit(value if "://" in value else f"//{value}")
    return parsed.hostname or ""


def _ensure_scheme(value, default_scheme="https"):
    """Ensure a value has a scheme (http/https).

    Many deployment environments may provide only a hostname (e.g. "example.com").
    Django requires a full origin (e.g. "https://example.com") for CSRF_TRUSTED_ORIGINS.
    """

    if not value:
        return value

    value = value.strip()
    parsed = urlsplit(value)
    if parsed.scheme:
        return value

    return f"{default_scheme}://{value}"


def _normalize_url_path(value, default="/"):
    """Normalize a URL path segment to ensure leading slash and no trailing slash."""

    path = (value or "").strip()
    if not path:
        return default

    if not path.startswith("/"):
        path = "/" + path

    # Keep "/" if that is the only path
    return path.rstrip("/") or "/"


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return str(value).lower() in ("1", "true", "yes", "on")


def _env_int(name, default):
    value = os.environ.get(name)
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_list(name, default=None):
    value = os.environ.get(name, "")
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or (default or [])


def _env_multiline_text(name, default=""):
    value = os.environ.get(name, "")
    if value.strip():
        return value.strip().replace("\\n", "\n")
    return default


def _join_base_url(base_url, path):
    normalized_base_url = (base_url or "").strip().rstrip("/")
    normalized_path = _normalize_url_path(path, default="/")
    if normalized_path == "/":
        return normalized_base_url or "/"
    return f"{normalized_base_url}{normalized_path}"


######################################################################
# General
######################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = str(os.environ.get("DEBUG", "true")).lower() in ("1", "true", "yes", "on")

SITE_URL = _ensure_scheme(os.environ.get("DJANGO_URL", "http://localhost").strip())
FRONTEND_URL = _ensure_scheme(
    os.environ.get("FRONTEND_URL", "http://localhost").strip()
)

ALLOWED_HOSTS = [
    host
    for host in [
        _clean_host(SITE_URL),
        _clean_host(FRONTEND_URL),
        *[_clean_host(host) for host in os.environ.get("ALLOWED_HOSTS", "").split(",")],
    ]
    if host
]

CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in [
        _ensure_scheme(SITE_URL).strip().rstrip("/"),
        _ensure_scheme(FRONTEND_URL).strip().rstrip("/"),
        *[
            _ensure_scheme(origin.strip().rstrip("/"))
            for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
        ],
    ]
    if origin
]

CORS_ALLOWED_ORIGINS = [
    origin
    for origin in [
        _ensure_scheme(FRONTEND_URL).strip().rstrip("/"),
        *[
            _ensure_scheme(origin.strip().rstrip("/"))
            for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
        ],
    ]
    if origin
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-session-token",
    "x-email-verification-key",
    "x-password-reset-key",
)

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
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Allauth
    "allauth",
    "allauth.account",
    "allauth.headless",
    "allauth.idp.oidc",
    # DRF
    "rest_framework",
    "drf_spectacular",
    # Third Party
    "corsheaders",
    "storages",
    # Users
    "users",
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
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH", "/usr/lib/libgdal.so")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH", "/usr/lib/libgeos_c.so")

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "TEST": {
            "NAME": "test",
        },
    }
}

######################################################################
# Authentication
######################################################################
AUTH_USER_MODEL = "users.User"

SITE_ID = _env_int("SITE_ID", 1)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

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
LOGIN_REDIRECT_URL = os.environ.get("LOGIN_REDIRECT_URL", "/")
LOGOUT_REDIRECT_URL = os.environ.get("LOGOUT_REDIRECT_URL", "/")

ACCOUNT_EMAIL_VERIFICATION = os.environ.get("ACCOUNT_EMAIL_VERIFICATION", "none")
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = _env_bool(
    "ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED", False
)
ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_CHANGE = _env_bool(
    "ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_CHANGE", False
)
ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND = _env_bool(
    "ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND", True
)
ACCOUNT_LOGIN_BY_CODE_ENABLED = _env_bool("ACCOUNT_LOGIN_BY_CODE_ENABLED", False)
ACCOUNT_LOGIN_BY_CODE_SUPPORTS_RESEND = _env_bool(
    "ACCOUNT_LOGIN_BY_CODE_SUPPORTS_RESEND", True
)
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = _env_bool(
    "ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED", False
)
ACCOUNT_SIGNUP_FORM_CLASS = "users.forms.AccountSignupForm"
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

HEADLESS_CLIENTS = tuple(_env_list("HEADLESS_CLIENTS", ["browser", "app"]))
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": _join_base_url(
        FRONTEND_URL, "/account/verify-email/{key}"
    ),
    "account_reset_password": _join_base_url(FRONTEND_URL, "/account/password/reset"),
    "account_reset_password_from_key": _join_base_url(
        FRONTEND_URL, "/account/password/reset/key/{key}"
    ),
    "account_signup": _join_base_url(FRONTEND_URL, "/account/signup"),
    "socialaccount_login_error": _join_base_url(
        FRONTEND_URL, "/account/provider/callback"
    ),
}
HEADLESS_ONLY = _env_bool("HEADLESS_ONLY", False)
HEADLESS_SERVE_SPECIFICATION = _env_bool("HEADLESS_SERVE_SPECIFICATION", False)

IDP_OIDC_PRIVATE_KEY = _env_multiline_text("OIDC_PRIVATE_KEY")

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
# Storages and Static/Media Files
######################################################################

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

USE_S3_STORAGE = _env_bool("S3_STORAGE_ENABLED", False)

if not USE_S3_STORAGE:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    s3_bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME", "").strip()
    s3_endpoint_url = os.environ.get("AWS_S3_ENDPOINT_URL", "").strip() or None
    s3_region_name = os.environ.get("AWS_S3_REGION_NAME", "").strip() or None
    s3_custom_domain = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "").strip() or None
    s3_default_acl = os.environ.get("AWS_DEFAULT_ACL", "").strip() or None
    s3_location = os.environ.get("AWS_LOCATION", "").strip()
    s3_url_protocol = (
        os.environ.get("AWS_S3_URL_PROTOCOL", "https:").strip() or "https:"
    )

    s3_options = {
        "bucket_name": s3_bucket_name,
        "access_key": os.environ.get("AWS_ACCESS_KEY_ID", "").strip() or None,
        "secret_key": os.environ.get("AWS_SECRET_ACCESS_KEY", "").strip() or None,
        "security_token": os.environ.get("AWS_SESSION_TOKEN", "").strip() or None,
        "region_name": s3_region_name,
        "endpoint_url": s3_endpoint_url,
        "custom_domain": s3_custom_domain,
        "default_acl": s3_default_acl,
        "querystring_auth": _env_bool("AWS_QUERYSTRING_AUTH", True),
        "querystring_expire": _env_int("AWS_QUERYSTRING_EXPIRE", 3600),
        "file_overwrite": _env_bool("AWS_S3_FILE_OVERWRITE", True),
        "location": s3_location,
        "url_protocol": s3_url_protocol,
        "addressing_style": os.environ.get("AWS_S3_ADDRESSING_STYLE", "").strip()
        or None,
    }
    s3_options = {
        option_name: option_value
        for option_name, option_value in s3_options.items()
        if option_value is not None
    }

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": s3_options,
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    media_url_override = os.environ.get("MEDIA_URL", "").strip()
    if media_url_override:
        MEDIA_URL = media_url_override
    elif s3_custom_domain:
        location_segment = f"/{s3_location.strip('/')}" if s3_location else ""
        MEDIA_URL = f"{s3_url_protocol}//{s3_custom_domain}{location_segment}/"


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
                        "link": reverse_lazy("admin:users_user_changelist"),
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
    print(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")
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
    print(f"SITE_ID: {SITE_ID}")
    print(f"LOGIN_URL: {LOGIN_URL}")
    print(f"LOGIN_REDIRECT_URL: {LOGIN_REDIRECT_URL}")
    print(f"LOGOUT_REDIRECT_URL: {LOGOUT_REDIRECT_URL}")
    print(f"LANGUAGE_CODE: {LANGUAGE_CODE}")
    print(f"TIME_ZONE: {TIME_ZONE}")
    print(f"USE_I18N: {USE_I18N}")
    print(f"USE_TZ: {USE_TZ}")
    print(f"STATIC_ROOT: {STATIC_ROOT}")
    print(f"STATIC_URL: {STATIC_URL}")
    print(f"MEDIA_ROOT: {MEDIA_ROOT}")
    print(f"AUTHENTICATION_BACKENDS: {AUTHENTICATION_BACKENDS}")
    print(f"ACCOUNT_LOGIN_METHODS: {ACCOUNT_LOGIN_METHODS}")
    print(f"ACCOUNT_SIGNUP_FIELDS: {ACCOUNT_SIGNUP_FIELDS}")
    print(
        "ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED: "
        f"{ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED}"
    )
    print(
        f"ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED: {ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED}"
    )
    print(f"HEADLESS_CLIENTS: {HEADLESS_CLIENTS}")
    print(f"HEADLESS_ONLY: {HEADLESS_ONLY}")
    print(f"IDP_OIDC_PRIVATE_KEY configured: {bool(IDP_OIDC_PRIVATE_KEY)}")
