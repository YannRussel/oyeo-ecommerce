import re

css_path = 'ecommerce/static/ecommerce/assets/css/partials/ProductsModelOne.css'
with open(css_path, 'r') as f:
    content = f.read()

content = re.sub(
    r'\.promo-label\s*\{[^}]*\}',
    '.promo-label {\n  display: inline-block;\n  flex: 0 0 auto;\n  background: #E60000 !important;\n  color: #fff !important;\n  font-size: 0.75rem !important;\n  padding: 4px 10px !important;\n  border-radius: 999px !important;\n  text-transform: uppercase !important;\n  font-weight: 700 !important;\n}',
    content
)

with open(css_path, 'w') as f:
    f.write(content)
print("Updated .promo-label CSS")
