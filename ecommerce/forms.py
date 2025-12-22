# core/forms.py
from django import forms

CURRENCY_CHOICES = [
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("XAF", "XAF"),
]

class PreSetupForm(forms.Form):
    # Admin
    admin_username = forms.CharField(label="Nom d'utilisateur admin", max_length=150)
    admin_email = forms.EmailField(label="Email admin")
    admin_password = forms.CharField(label="Mot de passe admin", widget=forms.PasswordInput)

    # Boutique
    shop_name = forms.CharField(label="Nom de la boutique", max_length=150)
    currency = forms.ChoiceField(label="Devise", choices=CURRENCY_CHOICES, initial="USD")

    # Catégories de base (optionnel)
    create_default_categories = forms.BooleanField(
        label="Créer des catégories de base (Femme, Homme, Enfant, ...)",
        required=False,
        initial=True
    )
