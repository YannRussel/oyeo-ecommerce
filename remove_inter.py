import os
import glob
import re

directory = 'ecommerce/templates/ecommerce'
files = glob.glob(os.path.join(directory, '**', '*.html'), recursive=True)

pattern = re.compile(r'[ \t]*<link href="https://fonts\.googleapis\.com/css2\?family=Inter[^\n]+rel="stylesheet">\n+<style>\n/\* Changer la police de tous les articles et détails pour Inter \*/\n.*?</style>', re.DOTALL)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = pattern.sub('', content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned {filepath}")
