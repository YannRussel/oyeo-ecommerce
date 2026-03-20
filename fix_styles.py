import re

css_path = 'ecommerce/static/ecommerce/assets/css/partials/ProductsModelOne.css'
with open(css_path, 'r') as f:
    content = f.read()

# Fix price-group
content = re.sub(
    r'\.price-group\s*\{[^}]*\}',
    '.price-group {\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  gap: 4px;\n}',
    content
)

# Replace specific styles in global rules if needed
if "flex-direction: column" not in content[:content.find(".price-group") + 200]:
    # if regex failed
    print("Regex might have failed")

with open(css_path, 'w') as f:
    f.write(content)
print("Updated .price-group in ProductsModelOne")
