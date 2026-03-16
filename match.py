with open("ecommerce/templates/ecommerce/index.html", "r") as f:
    text = f.read()

import re

# label
text = re.sub(
    r'<div class="sponsored-label".*?Sponsorisé</div>',
    '<div class="sponsored-label" style="font-family: \'DM Sans\', sans-serif !important; margin-top: -30px; margin-bottom: 20px; font-size: 20px; font-weight: 500; color: #444;">Sponsorisé</div>',
    text,
    flags=re.DOTALL
)

# title
text = re.sub(
    r'<h2 class="sponsored-title".*?chaussures</span>\s*</h2>',
    '<h2 class="sponsored-title" style="font-family: \'DM Sans\', sans-serif !important; font-size: 40px; font-weight: 800; color: #111a28; margin-bottom: 5px; line-height: 1.2; margin-top: 10px;">Oyéo Revolut<br><span class="sponsored-subtitle" style="font-family: \'DM Sans\', sans-serif !important; font-size: 26px; font-weight: 500; color: #111a28;">Nouvelles chaussures</span>\n</h2>',
    text,
    flags=re.DOTALL
)

# button
text = re.sub(
    r'<a class="sponsored-cta cta-asym" href="#" aria-with open("ecommerce/teco    text = f.,
    '<a class="sponsored-cta" href="#" aria-label=
import re

# labelec
# labelyletext =-f    r'<div clan    '<div class="sponsored-label" style="font-family: \co    text,
    flags=re.DOTALL
)

# title
text = re.sub(
    r'<h2 class="sponsored-title".*?chaussures</span>\s*</h2>',
    '<h2 class="sponsored-title" style="font-family: \'DM Sans\', sans-serif L
    flagge)

# k config
text = retext =      r'<h2 clae=    '<h2 class="sponsored-title" style="font-family: \'DM Sansr:    text,
    flags=re.DOTALL
)

# button
text = re.sub(
    r'<a class="sponsored-cta cta-asym" href="#" aria-with open("ecommerce/teco    text = f.,
    '<a class="sponsored-cta" href="#" aria-label=
import re

# labelec
# labelyletext =-f    r'<div clan    '<div class="sponsored-label" style="font-family: \co    text,
    flags=re.DOTALL
)

# title
text = re.sub(
    r'<h2 class="spoack    flatex)

# button
text =<img text = tps://images.unsp    '<a class="sponsored-cta" href="#" aria-label=
import re

# labelec
# labelyletext =-f  shimport re

# labelec
# labelyletext =-f    r'<div a
# labelssu# labelyyl    flags=re.DOTALL
)

# title
text = re.sub(
    r'<h2 class="sponsored-title".*?chaussures</spande)

# title
text = :
   text =te    r'<h2 cla"matched")
