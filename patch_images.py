import re

with open("ecommerce/templates/ecommerce/index.html", "r") as f:
    text = f.read()

# Pattern to find and remove the second image block
pattern = r"[ \t]+<!-- Bloc Image 2 -->\n[ \t]+<div style.*?<img src=.*?alt=\"Chaussure 2\".*?>\n[ \t]+</div>"

text = re.sub(pattern, "", text, flags=re.DOTALL)

with open("ecommerce/templates/ecommerce/index.html", "w") as f:
    f.write(text)
print("done removing image 2")
