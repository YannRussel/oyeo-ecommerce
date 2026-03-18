import re

with open("ecommerce/static/ecommerce/assets/css/unique/Home.css", "r") as f:
    text = f.read()

# First replace the bad block with a placeholder
pattern = r"  @keyframes nyota-uniq-scroll-left \{.*?\}[\s100%\{transform: translateX\(-50%\);\}\\n]*(?=  /\* reduced motion respecté \*/)"
clean_keyframes = """  @keyframes nyota-uniq-scroll-left {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
  }
"""

text = re.sub(pattern, clean_keyframes, text, flags=re.DOTALL)

with open("ecommerce/static/ecommerce/assets/css/unique/Home.css", "w") as f:
    f.write(text)
print("done cleaning")
