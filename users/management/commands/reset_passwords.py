# users/management/commands/reset_passwords.py

import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = (
        "Reset alle niet-superusers naar een random wachtwoord en schrijf ze naar CSV"
    )

    def handle(self, *args, **options):
        User = get_user_model()
        output_file = "new_passwords.csv"

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["username", "email", "password"])

            for user in User.objects.filter(is_superuser=False):
                plain_pw = get_random_string(12)
                user.password = make_password(plain_pw)
                user.save(update_fields=["password"])
                writer.writerow([user.username, user.email, plain_pw])

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Wachtwoorden gereset voor {User.objects.filter(is_superuser=False).count()} niet-superusers"
            )
        )
        self.stdout.write(f"👉 De plaintext-passwords vind je in {output_file}")
