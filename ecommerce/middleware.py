# core/middleware.py
from django.shortcuts import redirect
from .models import ShopSettings
from django.urls import reverse

EXEMPT_PATHS = [
    "/setup/",  # la page de setup
    "/admin/login/",
    "/admin/logout/",
    "/static/",
    "/media/",
]

class PreSetupMiddleware:
    """
    Redirige vers /setup/ si l'application n'est pas configurée encore.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # si déjà configuré -> passe
        if ShopSettings.objects.filter(is_configured=True).exists():
            return self.get_response(request)

        path = request.path
        # autoriser quelques chemins (login admin, static, setup)
        if any(path.startswith(p) for p in EXEMPT_PATHS) or path.startswith(reverse("ecommerce:pre_setup")):
            return self.get_response(request)

        return redirect("ecommerce:pre_setup")
