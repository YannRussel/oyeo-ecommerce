with open("ecommerce/static/ecommerce/assets/css/unique/Home.css", "r") as f:
    content = f.read()

content = content.replace("var(--nyota-uniq-start-offset)", "var(--nyota-uniq-start-offset, 0px)")

with open("ecommerce/static/ecommerce/assets/css/unique/Home.css", "w") as f:
    f.write(content)
print("done")
