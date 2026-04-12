import os
from urllib.parse import urlsplit

from allauth.idp.oidc.models import Client
from django.core.management.base import BaseCommand


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return str(value).lower() in ("1", "true", "yes", "on")


def _env_list(name, default=None):
    value = os.environ.get(name, "")
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or (default or [])


def _origin(value):
    parsed = urlsplit(value)
    if not parsed.scheme or not parsed.netloc:
        return ""
    return f"{parsed.scheme}://{parsed.netloc}"


class Command(BaseCommand):
    help = "Create or update the default allauth OIDC client from environment variables"

    def handle(self, *args, **options):
        client_id = os.environ.get("OIDC_CLIENT_ID", "").strip()
        client_secret = os.environ.get("OIDC_CLIENT_SECRET", "").strip()

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR(
                    "OIDC_CLIENT_ID and OIDC_CLIENT_SECRET are required"
                )
            )
            return

        redirect_uri = os.environ.get("REDIRECT_URI", "").strip()
        redirect_uris = _env_list("OIDC_REDIRECT_URIS", default=[redirect_uri])
        frontend_url = os.environ.get("FRONTEND_URL", "").strip()
        cors_origins = _env_list(
            "OIDC_CORS_ORIGINS",
            default=[_origin(frontend_url)] if frontend_url else [],
        )

        client = Client.objects.filter(pk=client_id).first()
        created = client is None
        if client is None:
            client = Client(id=client_id)

        client.name = os.environ.get("OIDC_CLIENT_NAME", "Frontend App").strip()
        client.type = Client.Type.CONFIDENTIAL
        client.skip_consent = _env_bool("OIDC_SKIP_CONSENT", True)
        client.set_secret(client_secret)
        client.set_redirect_uris(redirect_uris)
        client.set_cors_origins(cors_origins)
        client.set_scopes(["openid", "profile", "email"])
        client.set_default_scopes(["openid", "profile", "email"])
        client.set_grant_types(
            [
                Client.GrantType.AUTHORIZATION_CODE.value,
                Client.GrantType.REFRESH_TOKEN.value,
            ]
        )
        client.set_response_types(["code"])
        client.full_clean()
        client.save()

        message = "Created OIDC client" if created else "Updated OIDC client"
        self.stdout.write(self.style.SUCCESS(f"{message}: {client.id}"))