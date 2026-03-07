# ecommerce/templatetags/sections_tags.py
from django import template
from django.utils import timezone
from django.db.models import Prefetch, Q
from ..models import Section, ProductSection, ProductImage, Favorite

register = template.Library()

@register.inclusion_tag('ecommerce/partials/section_block.html', takes_context=True)
def render_section(context, section_slug, limit=8, show_see_more=True):
    """Rend un bloc section avec les produits valides pour ce slug."""
    now = timezone.now()
    ps_qs = ProductSection.objects.filter(
        section__slug=section_slug,
        is_active=True
    ).filter(
        Q(start_date__lte=now) | Q(start_date__isnull=True)
    ).filter(
        Q(end_date__gte=now) | Q(end_date__isnull=True)
    ).select_related('product', 'product__brand').order_by('order', '-created_at')

    main_image_qs = ProductImage.objects.filter(is_main=True)
    ps_qs = ps_qs.prefetch_related(Prefetch('product__images', queryset=main_image_qs, to_attr='prefetched_main_images'))

    section = Section.objects.filter(slug=section_slug, is_active=True).first()
    product_sections = list(ps_qs[:limit]) if section else []

    # Calcul des favoris
    user_favorites = set()
    request = context.get('request')
    if request and request.user.is_authenticated and product_sections:
        pks = [ps.product.pk for ps in product_sections]
        user_favorites = set(
            Favorite.objects.filter(user=request.user, product_id__in=pks)
            .values_list('product_id', flat=True)
        )

    return {
        'request': request,
        'section': section,
        'product_sections': product_sections,
        'show_see_more': show_see_more,
        'user_favorites': user_favorites,
    }
