import os, glob
files = glob.glob('ecommerce/static/ecommerce/assets/css/partials/ProductsModelOne*.css') + glob.glob('staticfiles/ecommerce/assets/css/partials/ProductsModelOne*.css')
for p in set(files):
    if not os.path.exists(p): continue
    with open(p, 'r') as f:
        c = f.read()
        if 'flex' in c: print('FOUND flex in', p.split('/')[-1])
