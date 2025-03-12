import os

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Creates a new OIDC client from environment variables"

    def handle(self, *args, **options):
        from oidc_provider.models import Client, ResponseType

        try:
            # Inicia una transacción para asegurar la atomicidad
            with transaction.atomic():
                # Obtiene o crea el ResponseType, evitando duplicados
                response_type, created = ResponseType.objects.get_or_create(
                    value="code"
                )

                # Crea el cliente
                c = Client(
                    name="{{cookiecutter.project_name}}",
                    client_id=os.environ.get("OIDC_CLIENT_ID"),
                    client_secret=os.environ.get("OIDC_CLIENT_SECRET"),
                    redirect_uris=[os.environ.get("REDIRECT_URI")],
                    reuse_consent=False
                )
                c.scope = ["openid", "profile", "email"]
                c.save()

                # Añade el ResponseType al cliente
                c.response_types.add(response_type)

                self.stdout.write(self.style.SUCCESS("Created OIDC Client"))
        except ResponseType.DoesNotExist:
            self.stdout.write(self.style.ERROR('ResponseType "code" does not exist'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error while creating OIDC Client: {e}")
            )
