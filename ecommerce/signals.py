# ecommerce/signals.py
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.db import transaction
from django.core.cache import cache
from .models import Category, MenuColumn, MenuColumnItem

MENU_CACHE_KEY = 'menu_structure_v2'

def _invalidate_menu_cache():
    cache.delete(MENU_CACHE_KEY)

def invalidate_menu_cache_on_commit():
    # supprime la clé APRÈS le commit de la transaction en cours
    transaction.on_commit(_invalidate_menu_cache)

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def category_changed(sender, **kwargs):
    invalidate_menu_cache_on_commit()

@receiver(post_save, sender=MenuColumn)
@receiver(post_delete, sender=MenuColumn)
def menu_column_changed(sender, **kwargs):
    invalidate_menu_cache_on_commit()

@receiver(post_save, sender=MenuColumnItem)
@receiver(post_delete, sender=MenuColumnItem)
def menu_column_item_changed(sender, **kwargs):
    invalidate_menu_cache_on_commit()

# pour changements sur le ManyToMany 'cards' de MenuColumn
@receiver(m2m_changed, sender=MenuColumn.cards.through)
def menu_column_cards_changed(sender, **kwargs):
    invalidate_menu_cache_on_commit()


# Pour le cote affichage Produit par section

# ecommerce/signals.py
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.db import transaction
from .models import ProductSection, Product, Section
from .cache_utils import delete_section_cache

def invalidate_after_commit(slug):
    def _del():
        delete_section_cache(slug)
    transaction.on_commit(_del)

@receiver(post_save, sender=ProductSection)
@receiver(post_delete, sender=ProductSection)
def productsection_changed(sender, instance, **kwargs):
    if instance.section:
        invalidate_after_commit(instance.section.slug)

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def product_changed(sender, instance, **kwargs):
    # supprimer cache pour toutes les sections liées à ce produit
    slugs = instance.sections.values_list('slug', flat=True)
    for s in slugs:
        invalidate_after_commit(s)

@receiver(post_save, sender=Section)
@receiver(post_delete, sender=Section)
def section_changed(sender, instance, **kwargs):
    invalidate_after_commit(instance.slug)
