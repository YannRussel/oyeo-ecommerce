import re
with open('ecommerce/templates/ecommerce/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_block = '''    <section class="promo-banner" style="background: #e2a42b; padding: 40px; border-radius: 0; display: flex; justify-content: space-between; align-items: flex-start; margin-top: 30px; margin-bottom: 30px; font-family: 'DM Sans', sans-serif;">
        <div class="promo-content" style="flex: 1; padding-top: 20px;">
            <div style="display: inline-block; background-color: #e26733; padding: 8px 15px; border-radius: 4px; margin-bottom: 5px;">
                <span style="color: white; font-weight: 700; font-family: 'DM Sans', sans-serif !important; font-size: 20px; letter-spacing: 0.5px; text-transform: uppercase;">DÉCOUVREZ LES MEILLEURES MARQUE</span>
            </div>
            <h2 class="promo-title" style="color: white; font-family: 'DM Sans', sans-serif !important; font-size: 24px; font-weight: 500; text-transform: uppercase; margin: 0; padding-left: 5px;">MARQUE POUR TOUS</h2>
        </div>

        <div class="promo-visual" style="display:flex; gap:30px; justify-content:flex-end; align-items:stretch;">
            <!-- Boîte blanche gauche -->
            <div class="promo-image shadow" style="background-color:#ffffff; width:250px; height:320px; border-radius:8px; box-shadow: 0 8px 18px rgba(0,0,0,0.05);"></div>

            <!-- Boîte blanche droite avec bouton 'Découvrir' -->
            <div style="position:relative; width:250px; height:320px;">
                <div class="promo-image shadow" style="background-color:#ffffff; width:100%; height:100%; border-radius:8px; box-shadow: 0 8px 18px rgba(0,0,0,0.05);"></div>
                <a href="#" class="promo-btn text-light" style="position:absolute; bottom:-20px; right:15px; background:#e16628; color:#fff; padding:12px 28px; border-radius:30px; font-weight:700; font-family: 'DM Sans', sans-serif !important; text-decoration:none; box-shadow:0 6px 16px rgba(0,0,0,0.15); font-size: 15px; z-index: 10;">Découvrir</a>
            </div>
        </div>
    </section>'''

# Replace the block
content = re.sub(r'<section class="promo-banner">.*?</section>', new_block, content, flags=re.DOTALL)

with open('ecommerce/templates/ecommerce/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('File updated successfully.')
