import re

files = [
    'ecommerce/templates/ecommerce/categorie.html',
    'ecommerce/templates/ecommerce/produit_detail.html',
    'ecommerce/templates/ecommerce/promotion.html',
    'ecommerce/templates/ecommerce/sousCategorie.html',
]

for p in files:
    with open(p, 'r') as f:
        c = f.read()
    
    # regex to eliminate multiple style attributes that are exactly identical next to each other
    c = c.replace("style=\"font-family: 'DM Sans', sans-serif !important;\" style=\"font-family: 'DM Sans', sans-serif !important;\"", "style=\"font-family: 'DM Sans', sans-serif !important;\"")
    c = c.replace("style=\"font-family: 'DM Sans', sans-serif !important;\" style=\"font-family: 'DM Sans', sans-serif !important;\"", "style=\"font-family: 'DM Sans', sans-serif !important;\"")
    
    with open(p, 'w') as f:
        f.write(c)
