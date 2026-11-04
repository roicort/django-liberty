import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Exit successfully when the configured superuser exists"

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        if not email:
            raise CommandError("DJANGO_SUPERUSER_EMAIL is required")

        user_model = get_user_model()
        if user_model.objects.filter(
            email__iexact=email,
            is_active=True,
            is_superuser=True,
        ).exists():
            return

        self.stdout.write(f"Configured superuser does not exist: {email}")
        raise SystemExit(10)
