from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def convert_price(value, currency_code):
    """
    Convertit une valeur (supposée en XAF base) vers la devise demandée.
    Taux fixe : 1 EUR = 655.957 XAF
    """
    if not value:
        return ""
    
    try:
        val = Decimal(value)
    except:
        return value

    # Si la devise cible est EUR
    if currency_code == 'EUR':
        # Conversion XAF -> EUR
        converted = val / Decimal("655.957")
        return f"{converted:.2f}".replace('.', ',')
    
    # Sinon (XAF ou autre), on formate simplement en millier
    # Format XAF classique : 10 000 (espace insécable souvent)
    # Ici simple string format
    return f"{val:,.0f}".replace(",", " ") 
