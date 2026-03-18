with open("ecommerce/templates/ecommerce/index.html", "r") as f:
    text = f.read()

# Replace the style width/height and remove border
old_string = 'style="width: 250px; height: 250px; background-color: #ffffff; border: 1.5px solid #14213d; display: flex; justify-content: center; align-items: center; padding: 15px; box-sizing: border-box;"'
new_string = 'style="width: 450px; height: 350px; background-color: #ffffff; display: flex; justify-content: center; align-items: center; padding: 15px; box-sizing: border-box;"'

text = text.replace(old_string, new_string)

with open("ecommerce/templates/ecommerce/index.html", "w") as f:
    f.write(text)
print("done patching block")
