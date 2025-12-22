from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Créer automatiquement un superutilisateur si inexistant"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write("⚠️ Variables ADMIN_* manquantes")
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write("✅ Superutilisateur créé")
        else:
            self.stdout.write("ℹ️ Superutilisateur déjà existant")
