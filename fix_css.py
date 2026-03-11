with open("ecommerce/static/ecommerce/assets/css/partials/ProductsModelOne.css", "r") as f:
    lines = f.readlines()

to_append = []
capture = False
for line in lines:
    if "#section-offres-du-jours" in line and "{" in line and not capture:
        capture = True
    if capture:
        pass # Handle differently because selectors are multiple lines sometimes.

