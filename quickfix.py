import os, glob
files = glob.glob('ecommerce/static/ecommerce/assets/css/partials/ProductsModelOne*.css') + glob.glob('staticfiles/ecommerce/assets/css/partials/ProductsModelOne*.css')
for p in set(files):
    if not os.path.exists(p): continue
    with open(p, 'r') as f: c = f.read()
    c = c.replace('flex: 0 0 360px !important;', 'flex: 0 0 260px !important;')
    c = c.replace('height: 260px !important;', 'height: 320px !important;')
    c = c.replace('flex: 0 0 320px !important;', 'flex: 0 0 230px !important;')
    c = c.replace('min-height: 360px !important;', 'min-height: 440px !important;')
    c = c.replace('height: 240px !important;', 'height: 300px !important;')
    c = c.replace('flex: 0 0 280px !important;', 'flex: 0 0 200px !important;')
    c = c.replace('height: 200px !important;', 'height: 160px !important;')
    with open(p, 'w') as f: f.write(c)
    print('Updated', p)
