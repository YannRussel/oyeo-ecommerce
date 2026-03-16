with open("ecommerce/templates/ecommerce/index.html", "r") as f:
    text = f.read()

old_string = 'style="width: 450px; height: 350px; background-color: #ffffff; display: flex; justify-content: center; align-items: center; padding: 15px; box-sizing: border-box;"'
new_string = 'style="width: 650px; height: 350px; background-color: transparent; display: flex; justify-content: center; align-items: center; padding: 0; box-sizing: border-box; overflow: hidden; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);"'

old_img = 'alt="Chaussure 1" style="width: 100%; height: 100%; object-fit: contain;"'
new_img = 'alt="Chaussure 1" style="width: 100%; height: 100%; object-fit: cover; border-radius: 20px;"'

text = text.replace(old_string, new_string)
text = text.replace(old_img, new_img)

with open("ecommerce/templates/ecommerce/index.html", "w") as f:
    f.write(text)
print("done rewriting precisely")
