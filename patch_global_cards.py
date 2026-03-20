import os

css_path = 'ecommerce/static/ecommerce/assets/css/partials/ProductsModelOne.css'
with open(css_path, 'r') as f:
    content = f.read()

# Add global rules for card text sizes
global_rules = """
/* Uniformisation des tailles selon "Offres du jour" pour toutes les grilles */
.product-card .product-title {
  font-weight: 700 !important;
  font-size: 1.25rem !important;
}

.product-card .brand {
  font-size: 0.95rem !important;
  font-weight: 700 !important;
}

.product-card .collection-name, .product-card .card-body p {
  font-size: 0.95rem !important;
}

.product-card .price {
  font-size: 1.2rem !important;
  font-weight: 800 !important;
}

.section-title {
  font-weight: 600 !important;
  font-size: 2rem !important;
}
"""

if "Uniformisation des tailles selon" not in content:
    content += "\n" + global_rules
    with open(css_path, 'w') as f:
        f.write(content)
    print("Patched ProductsModelOne.css")
else:
    print("Already patched")
