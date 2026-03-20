import re

css_path = 'ecommerce/templates/ecommerce/categorie.html'
with open(css_path, 'r') as f:
    content = f.read()

# Replace hardcoded heights for .img-wrap to inherit global responsive heights
content = re.sub(r'height:\s*320px;\s*/\* hauteur uniforme offres du jour \*/\s*', '', content)
content = re.sub(r'min-height:\s*420px;\s*/\* assure hauteur uniforme si le contenu varie \*/\s*', '', content)

with open(css_path, 'w') as f:
    f.write(content)
print("Removed fixed heights in categorie.html")
