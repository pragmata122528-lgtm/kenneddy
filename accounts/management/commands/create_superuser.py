"""
management command: create_superuser

Creates a superuser with the given credentials.

Usage:
    python manage.py create_superuser rafy 1234
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, Role


class Command(BaseCommand):
    help = "Create a superuser with given username and password"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username for the superuser")
        parser.add_argument("password", type=str, help="Password for the superuser")

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@kennedymoongrill.com",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "role": Role.ADMIN,
                    "full_name": username.capitalize(),
                    "phone": "0300-0000000",
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"[+] Superuser '{username}' created successfully.\n"
                    f"    Username: {username}\n"
                    f"    Password: {password}\n"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"[-] Superuser '{username}' already exists.\n"
                    f"    Username: {username}\n"
                )
            )

