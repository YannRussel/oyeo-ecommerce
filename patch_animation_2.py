import re

with open("ecommerce/static/ecommerce/assets/css/unique/Home.css", "r") as f:
    text = f.read()

text = re.sub(
    r"@keyframes nyota-uniq-scroll-left \{.*?\}",
    "@keyframes nyota-uniq-scroll-left {\n    0% { transform: translateX(0); }\n    100% { transform: translateX(-50%); }\n  }",
    text,
    flags=re.DOTALL
)

with open("ecommerce/static/ecommerce/assets/css/unique/Home.css", "w") as f:
    f.write(text)
print("patched keyframes to be extremely simple")
