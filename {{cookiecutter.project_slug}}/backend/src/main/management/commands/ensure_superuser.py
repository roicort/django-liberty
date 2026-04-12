import os

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the default superuser from environment variables"

    def handle(self, *args, **options):
        user_model = get_user_model()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "admin")
        last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "admin")

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD are required"
                )
            )
            return

        user, created = user_model.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        EmailAddress.objects.filter(user=user).exclude(email=user.email.lower()).update(
            primary=False
        )
        EmailAddress.objects.update_or_create(
            user=user,
            email=user.email.lower(),
            defaults={"primary": True, "verified": True},
        )

        message = "Created superuser" if created else "Updated superuser"
        self.stdout.write(self.style.SUCCESS(message))