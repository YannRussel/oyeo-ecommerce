# ecommerce/middleware_currency.py

class CurrencyMiddleware:
    """
    Middleware pour gérer la devise sélectionnée par l'utilisateur.
    Logique:
    1. Si 'devise' est dans les paramètres GET : mettre à jour la session.
    2. Lire la devise depuis la session (ou valeur par défaut).
    3. Exposer `request.currency` et `request.currency_symbol` aux vues/templates.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Vérification du paramètre GET
        devise_param = request.GET.get('devise')
        if devise_param in ['XAF', 'EUR']:
            request.session['currency'] = devise_param

        # 2. Récupération depuis la session (défaut: XAF)
        currency_code = request.session.get('currency', 'XAF')
        
        # S'assurer que la valeur est valide (au cas où la session aurait une vieille valeur)
        if currency_code not in ['XAF', 'EUR']:
            currency_code = 'XAF'
            request.session['currency'] = 'XAF'

        # 3. Exposition dans l'objet request
        request.currency = currency_code
        
        if currency_code == 'XAF':
            request.currency_symbol = 'FCFA'
        else:
            request.currency_symbol = '€'

        response = self.get_response(request)
        return response
