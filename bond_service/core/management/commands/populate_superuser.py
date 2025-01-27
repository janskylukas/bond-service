from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Creates a superuser"

    def handle(self, *args, **options):
        # Create the superuser
        call_command(
            "createsuperuser",
            interactive=False,
            username="admin",
            email="admin@example.com",
        )

        # Get the superuser object
        superuser = User.objects.get(username="admin")

        # Generate an API token for the superuser
        token, created = Token.objects.get_or_create(user=superuser)

        # Print the API token
        self.stdout.write(self.style.SUCCESS(f"API Token: {token.key}\n"))
