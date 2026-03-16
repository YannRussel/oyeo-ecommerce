from django.urls import path
from . import views

app_name = "ecommerce" 

urlpatterns = [
    # Exemple de route
    path('run-migrations/', views.run_migrations, name='run_migrations'),
    path('', views.acceuil, name='acceuil-site'),
    path('search/', views.search_view, name='search'),
    path('search/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('api/menu/', views.menu_api, name='menu_api'),
    path('sections/<slug:slug>/', views.section_list, name='section_list'),
    path('produit/<slug:slug>/', views.product_detail, name='product_detail'),
    # Liens vers cartes cadeaux
    path('carte-cadeaux', views.carte_cadeaux, name='carte-cadeaux'),
    path("setup/", views.pre_setup, name="pre_setup"),
    # Liens vers AntiGaspi
    path("anti-gaspi", views.antigaspi, name="antigaspi"),
    path("voir-offres-antigaspi", views.voirOffresAntigaspi, name="voir-offres-antigaspi"),
    path("supermarche-index", views.supermarche, name = "index-supermarche"),
    path("supermarche-rayon", views.suepermarche_rayon, name = "rayon-supermarche"),
    path("tous-les-rayons", views.supermarche_cat, name = "cat-supermarche"),
    # Vue Inscription
    path("inscription", views.inscription, name = "vue-inscription"),
    # Vue diaspora
    path("diaspora", views.diaspora, name = "vue-diaspora"),
        path("panier/", views.recap_panier, name="recap_panier"),
    path("checkout/", views.checkout, name="checkout"),

    path("ajax/cart/add/", views.add_to_cart, name="add_to_cart"),
    path("ajax/cart/update/", views.update_cart_quantity, name="update_cart_quantity"),
    path("ajax/cart/remove/", views.remove_from_cart, name="remove_from_cart"),
]
