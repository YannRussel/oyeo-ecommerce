import re
import os

files = [
    'ecommerce/templates/ecommerce/categorie.html',
    'ecommerce/templates/ecommerce/produit_detail.html',
    'ecommerce/templates/ecommerce/promotion.html',
    'ecommerce/templates/ecommerce/sousCategorie.html',
]
style = " style=\"font-family: 'DM Sans', sans-serif !important;\""

# Clean up specific formatting that the user mentioned
for path in files:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Headers
        content = re.sub(r'<h2([^>]*)>(Livraison Rapide et Sécurisée|Habillement de Jeune Fille|Fiable et Approuvé|Les Femmes et la mode|Fiable et Approuvé partout)</h2>', 
                         r'<h2\1' + style + r'>\2</h2>', content)
        
        # Paragraphs
        content = re.sub(r'<p([^>]*)>(Commandez vos articles en ligne et <br> recevez-les directement à votre porte.|Découvrez des denière fabrication <br> de la mode feminine.|Rejoignez une communauté croissante de clients satisfaits et en bonne santé.)</p>', 
                         r'<p\1' + style + r'>\2</p>', content)
        
        # Multi-line paragraphs
        content = re.sub(r'<p([^>]*)>\s*(Rejoignez une communauté croissante de clients <br> satisfaits et en\s*bonne santé.)\s*</p>', 
                         r'<p\1' + style + r'>\2</p>', content, flags=re.DOTALL)
                         
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
