import re
import os

files = [
    'ecommerce/templates/ecommerce/sousCategorie.html',
    'ecommerce/templates/ecommerce/supermarchecategorie.html',
    'ecommerce/templates/ecommerce/produit_detail.html',
    'ecommerce/templates/ecommerce/promotion.html',
]

for p in files:
    try:
        with open(p, 'r') as f:
            content = f.read()

        # Remove hardcoded heights
        content = re.sub(r'height:\s*\d+px;.*?(?:/\*.*?\*/)?', '', content)
        content = re.sub(r'min-height:\s*\d+px;.*?(?:/\*.*?\*/)?', '', content)
        
        with open(p, 'w') as f:
            f.write(content)
        print("Fixed", p)
    except Exception as e:
        print("Skipped", p, e)
