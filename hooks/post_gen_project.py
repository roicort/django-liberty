import secrets
import base64
import random
import json
import shutil
import os


context_str = r"""
{{ cookiecutter | jsonify }}
"""
context = json.loads(context_str)

project_slug = str(context.get("project_slug")).lower()
frontend = str(context.get("frontend")).lower()

oidc_client_id = random.randint(100000, 999999)
oidc_client_secret = secrets.token_hex(32)

DJANGO_URL = "http://backend:8000"
FRONTEND_URL = "http://frontend:3000"

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
        "OIDC_ISSUER": f"{DJANGO_URL}/oidc",
        "OIDC_WELL_KNOWN": f"{DJANGO_URL}/oidc/.well-known/openid-configuration",
    }
    dir_to_remove = "frontend-next"
    redirect_uri = f"{FRONTEND_URL}/auth/oidc/callback"

if frontend == "next":
    print("Generating .env files for Next")
    env_front_variables = {
        "API_URL": DJANGO_URL,
        "NEXTAUTH_URL": FRONTEND_URL,
        "AUTH_SECRET": secrets.token_urlsafe(32),
        "OIDC_CLIENT_ID": oidc_client_id,
        "OIDC_CLIENT_SECRET": oidc_client_secret,
        "OIDC_ISSUER": f"{DJANGO_URL}/oidc",
        "OIDC_WELL_KNOWN": f"{DJANGO_URL}/oidc/.well-known/openid-configuration",
    }
    dir_to_remove = "frontend-nuxt"
    redirect_uri = f"{FRONTEND_URL}/api/auth/callback/django"

print(f"Generating .env files for {project_slug} project")

env_back_variables = {
    # Django
    "DEBUG": True,
    "SECRET_KEY": secrets.token_urlsafe(32),
    # Postgres
    "DB_USER": project_slug,
    "DB_PASSWORD": secrets.token_urlsafe(32),
    "DB_DATABASE": project_slug,
    "DB_HOST": "db",
    "DB_PORT": 5432,
    # OIDC
    "OIDC_CLIENT_ID": oidc_client_id,
    "OIDC_CLIENT_SECRET": oidc_client_secret,
    "REDIRECT_URI": redirect_uri,
    # Django Admin
    "DJANGO_SUPERUSER_USERNAME": project_slug,
    "DJANGO_SUPERUSER_EMAIL": f"admin@{project_slug}.com",
    "DJANGO_SUPERUSER_PASSWORD": secrets.token_urlsafe(32),
    # URLs
    "DJANGO_URL": DJANGO_URL,
    "FRONTEND_URL": FRONTEND_URL,
}

with open(".env", "w") as f:
    for key, value in env_back_variables.items():
        f.write(f"{key}={value}\n")

with open(".env.frontend", "w") as f:
    for key, value in env_front_variables.items():
        f.write(f"{key}={value}\n")

if dir_to_remove and os.path.exists(dir_to_remove):
    shutil.rmtree(dir_to_remove)

if os.path.exists("django-liberty"):
    shutil.rmtree("django-liberty")
