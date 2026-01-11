# ecommerce/views.py

import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Prefetch, Q, Case, When, Value, IntegerField
from django.db.models import F

from .models import (
    SliderImage,
    Category,
    CategorySlugHistory,
    Product,
    ProductImage,
    Section,
    ProductSection,
    Favorite,
)

# core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction

from .forms import PreSetupForm
from .models import ShopSettings
from ecommerce.utils import create_default_sections
from django.utils.text import slugify



from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required
import io


def run_migrations(request):
    """
    Exécute makemigrations + migrate depuis une URL
    (réservé aux utilisateurs staff)
    """
    output = io.StringIO()

    try:
        call_command('makemigrations', stdout=output, stderr=output)
        call_command('migrate', stdout=output, stderr=output)
    except Exception as e:
        return HttpResponse(
            f"<h1>Erreur migration</h1><pre>{str(e)}</pre>",
            status=500
        )

    return HttpResponse(
        "<h1>Migrations exécutées avec succès</h1>"
        "<pre>" + output.getvalue() + "</pre>"
    )
# ------------------------
# Helpers
# ------------------------
def build_breadcrumbs(category):
    """
    Construit le fil d’Ariane en remontant la hiérarchie des catégories.
    Retourne une liste ordered root->leaf : [{label, url}, ...]
    """
    crumbs = []
    current = category
    while current:
        crumbs.append({
            "label": current.name,
            "url": current.get_absolute_url()
        })
        current = current.parent
    crumbs.reverse()
    return crumbs


def _get_user_favorites_for_product_ids(user, product_ids):
    """
    Retourne un set d'ids de produits favoris pour l'utilisateur donné.
    Si user est anonymous, retourne set() rapidement.
    """
    if not user.is_authenticated or not product_ids:
        return set()
    return set(Favorite.objects.filter(user=user, product_id__in=product_ids).values_list('product_id', flat=True))


def get_leaf_categories(category):
    """
    Retourne la liste des catégories feuilles (objets Category)
    sous `category` (inclut `category` si elle est feuille).
    """
    leaves = []

    def walk(cat):
        children_qs = cat.children.filter(is_active=True)
        if not children_qs.exists():
            leaves.append(cat)
        else:
            for child in children_qs:
                walk(child)

    walk(category)
    return leaves


# ------------------------
# Accueil
# ------------------------
def acceuil(request):
    """
    Récupère les images du slider via le manager custom.
    Passe 'images' au template pour affichage.
    """
    images = SliderImage.objects.get_slider_images(limit=5)

    context = {
        'images': images,
    }
    return render(request, 'ecommerce/index.html', context)


# ------------------------
# Category detail (overview or product listing)
# ------------------------
def category_detail(request, slug):
    """
    Affiche les sous-catégories ET/OU les produits d'une catégorie.
    Les produits listés comprennent ceux dont la primary_category OU la M2M 'categories'
    est une catégorie feuille descendant de la catégorie demandée.
    L'affichage des produits est aléatoire et paginé.
    De plus : calcule une liste 'featured_products' basée sur les enfants directs de la catégorie.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    # Sous-catégories directes (pour affichage en haut de page, menu, etc.)
    children = category.children.filter(is_active=True).order_by('order', 'name')
    breadcrumbs = build_breadcrumbs(category)

    # --- récupérer les catégories feuilles (sous la catégorie sélectionnée) ---
    leaf_categories = get_leaf_categories(category)
    leaf_ids = [c.pk for c in leaf_categories]

    # --- Produits "A la une" : produits liés aux catégories ENFANTS (et leurs feuilles) ---
    direct_children = category.children.filter(is_active=True).order_by('order', 'name')

    child_leaf_ids = []
    for ch in direct_children:
        leaves = get_leaf_categories(ch)
        child_leaf_ids.extend([c.pk for c in leaves])

    featured_products = Product.objects.none()
    featured_favorites = set()

    if child_leaf_ids:
        featured_base_qs = Product.objects.filter(
            Q(primary_category__in=child_leaf_ids) | Q(categories__in=child_leaf_ids),
            is_active=True
        ).distinct().select_related('brand', 'primary_category')

        featured_ids = list(featured_base_qs.values_list('pk', flat=True))
        if featured_ids:
            sample_limit = min(len(featured_ids), 12)
            sampled_ids = random.sample(featured_ids, k=sample_limit) if len(featured_ids) > sample_limit else featured_ids

            order_expr = Case(
                *[When(pk=pk, then=Value(i)) for i, pk in enumerate(sampled_ids)],
                output_field=IntegerField()
            )

            main_img_qs = ProductImage.objects.filter(is_main=True)
            featured_products = (
                Product.objects.filter(pk__in=sampled_ids)
                .annotate(_rand_order=order_expr)
                .order_by('_rand_order')
                .prefetch_related(Prefetch('images', queryset=main_img_qs, to_attr='prefetched_main_images'))
                .select_related('brand', 'primary_category')
            )

            featured_product_ids = [p.pk for p in featured_products]
            featured_favorites = _get_user_favorites_for_product_ids(request.user, featured_product_ids)

    # --- queryset de base : primary_category OU categories (M2M) ---
    base_qs = Product.objects.filter(
        Q(primary_category__in=leaf_ids) | Q(categories__in=leaf_ids),
        is_active=True
    ).distinct().select_related('brand', 'primary_category')

    product_ids = list(base_qs.values_list('pk', flat=True))

    if not product_ids:
        breadcrumbs.append({"label": "0 Articles", "url": None})
        return render(request, 'ecommerce/categorie.html', {
            'category': category,
            'children': children,
            'products': [],
            'page_obj': None,
            'breadcrumbs': breadcrumbs,
            'user_favorites': set(),
            'featured_products': featured_products,
            'featured_favorites': featured_favorites,
        })

    # Mélange aléatoire des ids (en Python)
    random_ids = random.sample(product_ids, k=len(product_ids))

    # Conserver l'ordre aléatoire en SQL via CASE WHEN
    order_expr = Case(
        *[When(pk=pk, then=Value(i)) for i, pk in enumerate(random_ids)],
        output_field=IntegerField()
    )

    main_img_qs = ProductImage.objects.filter(is_main=True)

    products_qs = (
        Product.objects.filter(pk__in=random_ids)
        .annotate(_rand_order=order_expr)
        .order_by('_rand_order')
        .prefetch_related(Prefetch('images', queryset=main_img_qs, to_attr='prefetched_main_images'))
        .select_related('brand', 'primary_category')
    )

    # pagination (ajuste le nombre par page si besoin)
    paginator = Paginator(products_qs, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    page_product_ids = [p.pk for p in page_obj.object_list]
    user_favorites = _get_user_favorites_for_product_ids(request.user, page_product_ids)

    breadcrumbs.append({"label": f"{len(product_ids)} Articles", "url": None})

    return render(request, 'ecommerce/categorie.html', {
        'category': category,
        'children': children,
        'products': page_obj.object_list,  # liste des produits à afficher
        'page_obj': page_obj,
        'breadcrumbs': breadcrumbs,
        'user_favorites': user_favorites,
        'featured_products': featured_products,
        'featured_favorites': featured_favorites,
    })


# ------------------------
# Section list (paged)
# ------------------------
def section_list(request, slug):
    """
    Liste paginée des ProductSection actifs pour une section.
    Passe page_obj (page d'objets ProductSection) ET product_sections (liste) et user_favorites.
    """
    section = get_object_or_404(Section, slug=slug, is_active=True)
    now = timezone.now()

    # queryset ProductSection valides pour cette section
    ps_qs = ProductSection.objects.filter(
        section=section,
        is_active=True
    ).filter(
        Q(start_date__lte=now) | Q(start_date__isnull=True),
        Q(end_date__gte=now) | Q(end_date__isnull=True)
    ).select_related('product', 'product__brand').order_by('order', '-created_at')

    # précharger l'image principale si tu utilises ProductImage.is_main
    main_img_qs = ProductImage.objects.filter(is_main=True)
    ps_qs = ps_qs.prefetch_related(Prefetch('product__images', queryset=main_img_qs, to_attr='prefetched_main_images'))

    # pagination (ex : 24 produits par page)
    paginator = Paginator(ps_qs, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Récupère les product ids présents sur la page (pour calculer user_favorites)
    product_ids = [ps.product_id for ps in page_obj.object_list]
    user_favorites = _get_user_favorites_for_product_ids(request.user, product_ids)

    context = {
        'section': section,
        'page_obj': page_obj,          # page d'objets ProductSection
        'product_sections': page_obj.object_list,  # compatibilité templates
        'user_favorites': user_favorites,
    }
    return render(request, 'ecommerce/section_list.html', context)


# ------------------------
# Product detail
# ------------------------
def product_detail(request, slug):
    """
    Détail produit : récupère le product par slug et précharge l'image principale.
    Fournit aussi is_favorited pour le user connecté.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # précharger l'image principale si tu utilises ProductImage.is_main
    main_img_qs = ProductImage.objects.filter(is_main=True)
    product = Product.objects.filter(pk=product.pk).prefetch_related(
        Prefetch('images', queryset=main_img_qs, to_attr='prefetched_main_images')
    ).select_related('brand', 'primary_category').first()

    if not product:
        product = get_object_or_404(Product, slug=slug, is_active=True)

    # état favori pour le produit
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'is_favorited': is_favorited,
    }
    return render(request, 'ecommerce/product_detail.html', context)


# ------------------------
# Toggle favorite (AJAX)
# ------------------------
@require_POST
@login_required
def toggle_favorite(request):
    """
    Toggle favorite via AJAX.
    Accepte JSON ou form-data. Retourne JSON: {'favorited': bool, 'count': int, 'product_id': id}
    """
    # support JSON body ou form-data
    if request.content_type == 'application/json':
        try:
            payload = json.loads(request.body.decode())
        except Exception:
            return HttpResponseBadRequest("JSON invalide")
        product_id = payload.get('product_id')
    else:
        product_id = request.POST.get('product_id')

    if not product_id:
        return HttpResponseBadRequest("product_id manquant")

    product = get_object_or_404(Product, pk=product_id)

    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        # existait déjà -> supprimer (toggle off)
        fav.delete()
        favorited = False
    else:
        favorited = True

    count = Favorite.objects.filter(product=product).count()
    return JsonResponse({'favorited': favorited, 'count': count, 'product_id': product.pk})
# ------------------------
# Menu API (si utilisé)
# ------------------------
def menu_api(request):
    from .context_processors import build_menu_structure
    return JsonResponse(build_menu_structure(), safe=False, json_dumps_params={'ensure_ascii': False})


# Liens vers cartes cadeaux
def carte_cadeaux(request):
    return render(request, 'ecommerce/Oyéo_cartes cadeaux.html')

# Vue pour la PRE-CONFIGURATION

User = get_user_model()

@transaction.atomic
def pre_setup(request):
    # Si déjà configuré -> redirige vers l'accueil
    if ShopSettings.objects.filter(is_configured=True).exists():
        return redirect("home")  # adapte le nom de la vue home

    if request.method == "POST":
        form = PreSetupForm(request.POST)
        if form.is_valid():
            # créer le superuser
            username = form.cleaned_data["admin_username"]
            email = form.cleaned_data["admin_email"]
            password = form.cleaned_data["admin_password"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Le nom d'utilisateur existe déjà. Choisissez-en un autre.")
            else:
                user = User.objects.create_superuser(username=username, email=email, password=password)

                # créer ShopSettings
                shop = ShopSettings.objects.create(
                    shop_name=form.cleaned_data["shop_name"],
                    currency=form.cleaned_data["currency"],
                    is_configured=True
                )

                # créer sections par défaut
                create_default_sections()

                # si tu veux créer des catégories de base, tu peux le faire ici (optionnel)
                if form.cleaned_data.get("create_default_categories"):
                    from ecommerce.models import Category
                    defaults = ["Femme", "Homme", "Enfant", "Électronique"]
                    for name in defaults:
                        Category.objects.get_or_create(name=name, slug=slugify(name), defaults={"is_active": True, "is_fixed": True})

                messages.success(request, "Configuration terminée — connectez-vous avec l'administrateur créé.")
                return redirect("admin:login")
    else:
        form = PreSetupForm()

    return render(request, "ecommerce/pre_setup.html", {"form": form})

# Vue vers AntiGaspi

def antigaspi(request) :
    return render(request, 'ecommerce/antigaspi1.html')

def voirOffresAntigaspi(request) :

    return render(request, 'ecommerce/antigaspi-voir-offres.html', {})

# Vue supermarché

def supermarche(request) :
    return render(request, 'ecommerce/supermarche.html')