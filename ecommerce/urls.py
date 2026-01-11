from django.urls import path
from . import views

app_name = "ecommerce" 

urlpatterns = [
    # Exemple de route
    path('run-migrations/', views.run_migrations, name='run_migrations'),
    path('', views.acceuil, name='acceuil-site'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('api/menu/', views.menu_api, name='menu_api'),
    path('sections/<slug:slug>/', views.section_list, name='section_list'),
    path('produit/<slug:slug>/', views.product_detail, name='product_detail'),
    path('ajax/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    # Liens vers cartes cadeaux
    path('carte-cadeaux', views.carte_cadeaux, name='carte-cadeaux'),
    path("setup/", views.pre_setup, name="pre_setup"),
    # Liens vers AntiGaspi
    path("anti-gaspi", views.antigaspi, name="antigaspi"),
    path("voir-offres-antigaspi", views.voirOffresAntigaspi, name="voir-offres-antigaspi"),
    path("supermarche-index", views.supermarche, name = "index-supermarche")
]
