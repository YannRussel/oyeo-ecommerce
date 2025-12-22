# ecommerce/utils.py
from django.utils import timezone
from django.db.models import Prefetch, Q
from .models import Section, ProductSection, ProductImage

def get_sections_with_products(slugs=None, limit_per_section=8):
    """
    Récupère les sections actives et précharge les ProductSection actuels
    et les products associés. `slugs` (list) permet de filtrer si besoin.
    Retourne une list d'objets Section avec attribut `prefetched_product_sections`.
    """
    now = timezone.now()

    # queryset des ProductSection valides (filtre période + is_active)
    ps_qs = ProductSection.objects.filter(
        is_active=True
    ).filter(
        Q(start_date__lte=now) | Q(start_date__isnull=True)
    ).filter(
        Q(end_date__gte=now) | Q(end_date__isnull=True)
    ).select_related('product', 'product__brand').order_by('order', '-created_at')

    # Préfetch l'image principale du produit (optimisation)
    main_image_qs = ProductImage.objects.filter(is_main=True)

    # Prefetch product.images into attribute on product (optional)
    # We'll attach images to product via prefetch on Product (through product in ProductSection)
    ps_qs = ps_qs.prefetch_related(Prefetch('product__images', queryset=main_image_qs, to_attr='prefetched_main_images'))

    sections_qs = Section.objects.filter(is_active=True).order_by('order', 'name')
    if slugs:
        sections_qs = sections_qs.filter(slug__in=slugs)

    sections_qs = sections_qs.prefetch_related(
        Prefetch('product_sections', queryset=ps_qs, to_attr='prefetched_product_sections')
    )

    # Limiter manuellement le nombre de produits par section (on le fera en template ou en code)
    sections = list(sections_qs)
    for sec in sections:
        sec.prefetched_product_sections = sec.prefetched_product_sections[:limit_per_section]
    return sections
