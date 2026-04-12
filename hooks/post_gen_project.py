import secrets
import base64
import random
import json
import shutil
import os
import subprocess


context_str = r"""
{{ cookiecutter | jsonify }}
"""
context = json.loads(context_str)

project_slug = str(context.get("project_slug")).lower()
frontend = str(context.get("frontend")).lower()
backend_env_path = os.path.join("backend", ".env")
frontend_dir = "frontend"
frontend_env_path = os.path.join(frontend_dir, ".env")

oidc_client_id = random.randint(100000, 999999)
oidc_client_secret = secrets.token_hex(32)
postgres_user = project_slug
postgres_password = secrets.token_urlsafe(32)
postgres_db = project_slug


def generate_oidc_private_key():
    try:
        result = subprocess.run(
            [
                "openssl",
                "genpkey",
                "-algorithm",
                "RSA",
                "-pkeyopt",
                "rsa_keygen_bits:2048",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "openssl is required to generate the OIDC private key"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("failed to generate the OIDC private key") from exc

    return result.stdout.strip().replace("\n", "\\n")


DJANGO_URL = "http://backend:8000"
FRONTEND_URL = "http://frontend:3000"
oidc_private_key = generate_oidc_private_key()

if frontend == "nuxt":
    print("Generating .env files for Nuxt")
    env_front_variables = {
        "API_URL": DJANGO_URL,
        "NUXT_API_SECRET": secrets.token_urlsafe(32),
        "NUXT_OIDC_TOKEN_KEY": base64.b64encode(secrets.token_bytes(32)).decode(
            "utf-8"
        ),  # base64_encoded_key
        "NUXT_OIDC_SESSION_SECRET": secrets.token_urlsafe(
            36
        ),  # 48_characters_random_string
        "NUXT_OIDC_AUTH_SESSION_SECRET": secrets.token_urlsafe(
            36
        ),  # 48_characters_random_string
        "OIDC_CLIENT_ID": oidc_client_id,
        "OIDC_CLIENT_SECRET": oidc_client_secret,
        "OIDC_ISSUER": DJANGO_URL,
        "OIDC_WELL_KNOWN": f"{DJANGO_URL}/.well-known/openid-configuration",
    }
    redirect_uri = f"{FRONTEND_URL}/auth/oidc/callback"

if frontend == "next":
    print("Generating .env files for Next")
    auth_secret = secrets.token_urlsafe(32)
    env_front_variables = {
        "API_URL": DJANGO_URL,
        "NEXTAUTH_URL": FRONTEND_URL,
        "AUTH_SECRET": auth_secret,
        "NEXTAUTH_SECRET": auth_secret,
        "OIDC_CLIENT_ID": oidc_client_id,
        "OIDC_CLIENT_SECRET": oidc_client_secret,
        "OIDC_ISSUER": DJANGO_URL,
        "OIDC_WELL_KNOWN": f"{DJANGO_URL}/.well-known/openid-configuration",
    }
    redirect_uri = f"{FRONTEND_URL}/api/auth/callback/django"

print(f"Generating .env files for {project_slug} project")

env_back_variables = {
    # Django
    "DEBUG": True,
    "SECRET_KEY": secrets.token_urlsafe(32),
    # Postgres
    "POSTGRES_USER": postgres_user,
    "POSTGRES_PASSWORD": postgres_password,
    "POSTGRES_DB": postgres_db,
    "POSTGRES_HOST": "database",
    "POSTGRES_PORT": 5432,
    # OIDC
    "OIDC_CLIENT_ID": oidc_client_id,
    "OIDC_CLIENT_SECRET": oidc_client_secret,
    "OIDC_CLIENT_NAME": f"{project_slug}-frontend",
    "OIDC_CORS_ORIGINS": FRONTEND_URL,
    "OIDC_PRIVATE_KEY": oidc_private_key,
    "OIDC_REDIRECT_URIS": redirect_uri,
    "OIDC_SKIP_CONSENT": True,
    "REDIRECT_URI": redirect_uri,
    # Allauth account/headless
    "ACCOUNT_EMAIL_VERIFICATION": "none",
    "ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED": False,
    "ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_CHANGE": False,
    "ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND": True,
    "ACCOUNT_LOGIN_BY_CODE_ENABLED": False,
    "ACCOUNT_LOGIN_BY_CODE_SUPPORTS_RESEND": True,
    "ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED": False,
    "CORS_ALLOWED_ORIGINS": FRONTEND_URL,
    "HEADLESS_CLIENTS": "browser,app",
    "HEADLESS_ONLY": False,
    "HEADLESS_SERVE_SPECIFICATION": False,
    # Django Admin
    "DJANGO_SUPERUSER_USERNAME": project_slug,
    "DJANGO_SUPERUSER_EMAIL": f"admin@{project_slug}.com",
    "DJANGO_SUPERUSER_PASSWORD": secrets.token_urlsafe(32),
    # URLs
    "DJANGO_URL": DJANGO_URL,
    "FRONTEND_URL": FRONTEND_URL,
    # GDAL
    "GDAL_LIBRARY_PATH": "/usr/lib/libgdal.so",
    "GEOS_LIBRARY_PATH": "/usr/lib/libgeos_c.so",
    "#GDAL_LIBRARY_PATH": "/opt/homebrew/bin/gdal",
    "#GEOS_LIBRARY_PATH": "/opt/homebrew/bin/geosop",
}

os.makedirs("backend", exist_ok=True)
os.makedirs(frontend_dir, exist_ok=True)

with open(backend_env_path, "w") as f:
    for key, value in env_back_variables.items():
        f.write(f"{key}={value}\n")

with open(frontend_env_path, "w") as f:
    for key, value in env_front_variables.items():
        f.write(f"{key}={value}\n")

if os.path.exists("django-liberty"):
    shutil.rmtree("django-liberty")
