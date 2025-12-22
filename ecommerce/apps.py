# ecommerce/apps.py
from django.apps import AppConfig

class EcommerceConfig(AppConfig):
    name = "ecommerce"

    def ready(self):
        # importe les handlers pour les connecter
        from . import signals  # noqa: F401
