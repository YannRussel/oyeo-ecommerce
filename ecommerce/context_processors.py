# ecommerce/context_processors.py

import json
import logging
from django.core.cache import cache
from django.db.models import Prefetch
from .models import Category, MenuColumn, MenuColumnItem

logger = logging.getLogger(__name__)


def _chunk_list(lst, n):
    if not lst:
        return [[] for _ in range(n)]
    k, m = divmod(len(lst), n)
    chunks = []
    i = 0
    for _ in range(n):
        size = k + (1 if m > 0 else 0)
        chunks.append(lst[i:i + size])
        i += size
        if m:
            m -= 1
    return chunks


def build_menu_structure():
    """
    Construit la structure du menu avec champs supplémentaires pré-calculés pour le template :
    - top_entry contient 'is_fixed'
    - sub_entry contient 'items_flat' (liste dédupliquée) et 'cards' (pour "À la une")
    """
    cache_key = 'menu_structure_v2'
    cached = cache.get(cache_key)
    if cached:
        return cached

    menu = []
    try:
        # Prefetch configuration (inchangée)
        menu_items_prefetch = Prefetch(
            'menu_items',
            queryset=MenuColumnItem.objects.select_related('category').order_by('order'),
            to_attr='prefetched_menu_items'
        )
        menu_columns_qs = MenuColumn.objects.all().prefetch_related(menu_items_prefetch, 'cards').order_by('order')

        tops_qs = Category.objects.filter(parent__isnull=True, is_active=True).order_by('order', 'name').prefetch_related(
            Prefetch(
                'children',
                queryset=Category.objects.filter(is_active=True).order_by('order', 'name').prefetch_related(
                    Prefetch('children', queryset=Category.objects.filter(is_active=True).order_by('order', 'name')),
                    Prefetch('menu_columns', queryset=menu_columns_qs, to_attr='prefetched_menu_columns')
                ),
                to_attr='prefetched_children'
            )
        )

        for top in tops_qs:
            top_entry = {
                "title": top.name,
                "slug": top.slug,
                "url": getattr(top, "get_absolute_url", lambda: "")(),
                "children": [],
                "is_fixed": getattr(top, "is_fixed", False),
            }

            subs = getattr(top, 'prefetched_children', None) or list(top.children.all())

            for sub in subs:
                columns = []
                menu_cols = getattr(sub, 'prefetched_menu_columns', None) or list(sub.menu_columns.all())

                if menu_cols:
                    for mc in menu_cols:
                        heading = mc.heading or mc.get_column_type_display()
                        if mc.column_type in ('list', 'brands'):
                            items = []
                            prefetched_items = getattr(mc, 'prefetched_menu_items', None)
                            if prefetched_items is not None:
                                for mi in prefetched_items:
                                    if not mi.is_active:
                                        continue
                                    cat = mi.category
                                    items.append({"title": cat.name, "url": getattr(cat, "get_absolute_url", lambda: "")()})
                            else:
                                for mi in mc.menu_items.select_related('category').filter(is_active=True).order_by('order'):
                                    cat = mi.category
                                    items.append({"title": cat.name, "url": getattr(cat, "get_absolute_url", lambda: "")()})
                            columns.append({"heading": heading, "items": items})

                        elif mc.column_type == 'cards':
                            cards = []
                            prefetched_items = getattr(mc, 'prefetched_menu_items', None)
                            if prefetched_items is not None:
                                card_items = [mi for mi in prefetched_items if mi.is_card and mi.is_active]
                                if not card_items:
                                    for c in mc.cards.all()[:4]:
                                        img = c.thumbnail.url if getattr(c, 'thumbnail', None) else ""
                                        cards.append({"title": c.name, "url": getattr(c, "get_absolute_url", lambda: "")(), "image": img})
                                else:
                                    for mi in card_items[:4]:
                                        c = mi.category
                                        img = c.thumbnail.url if getattr(c, 'thumbnail', None) else ""
                                        cards.append({"title": c.name, "url": getattr(c, "get_absolute_url", lambda: "")(), "image": img})
                            else:
                                card_items_qs = mc.menu_items.select_related('category').filter(is_active=True, is_card=True).order_by('order')[:4]
                                if card_items_qs.exists():
                                    for mi in card_items_qs:
                                        c = mi.category
                                        img = c.thumbnail.url if getattr(c, 'thumbnail', None) else ""
                                        cards.append({"title": c.name, "url": getattr(c, "get_absolute_url", lambda: "")(), "image": img})
                                else:
                                    for c in mc.cards.all()[:4]:
                                        img = c.thumbnail.url if getattr(c, 'thumbnail', None) else ""
                                        cards.append({"title": c.name, "url": getattr(c, "get_absolute_url", lambda: "")(), "image": img})
                            columns.append({"heading": heading or "A la une", "cards": cards})

                        else:
                            # fallback as list
                            items = []
                            prefetched_items = getattr(mc, 'prefetched_menu_items', None)
                            if prefetched_items is not None:
                                for mi in prefetched_items:
                                    if not mi.is_active:
                                        continue
                                    cat = mi.category
                                    items.append({"title": cat.name, "url": getattr(cat, "get_absolute_url", lambda: "")()})
                            columns.append({"heading": heading, "items": items})
                else:
                    # fallback chunk (inchangé)
                    grands = getattr(sub, 'children', None)
                    if grands is None:
                        grands = list(sub.children.all())
                    else:
                        if hasattr(grands, 'all'):
                            grands = list(grands.all())
                        else:
                            try:
                                grands = list(grands)
                            except Exception:
                                grands = []

                    items = [{"title": g.name, "url": getattr(g, "get_absolute_url", lambda: "")()} for g in grands]
                    cols = _chunk_list(items, 3)
                    headings = ["Tout Voir", "Inspections", "Marques à l'honneur"]
                    for i, col_items in enumerate(cols):
                        columns.append({"heading": headings[i] if i < len(headings) else "", "items": col_items})

                    featured_candidates = [g for g in grands if getattr(g, 'thumbnail', None)]
                    if not featured_candidates:
                        featured_candidates = grands
                    cards = [{"title": g.name, "url": getattr(g, "get_absolute_url", lambda: "")(), "image": (g.thumbnail.url if getattr(g, 'thumbnail', None) else "")} for g in featured_candidates[:4]]
                    columns.append({"heading": "A la une", "cards": cards})

                # --- Pré-calculs utiles pour le template ---
                # items_flat : liste unique (dédupliquée) d'items (ordre préservé)
                seen = set()
                flat_items = []
                for col in columns:
                    for it in col.get('items', []) or []:
                        key = (it.get('url'), it.get('title'))
                        if key not in seen:
                            seen.add(key)
                            flat_items.append(it)

                # cards_list : préférer la 1ère colonne qui a des 'cards', sinon chercher items avec image
                cards_list = []
                for col in columns:
                    if col.get('cards'):
                        cards_list = col.get('cards')[:4]
                        break
                if not cards_list:
                    for col in columns:
                        for it in col.get('items', []):
                            if it.get('image'):
                                cards_list.append(it)
                                if len(cards_list) >= 4:
                                    break
                        if len(cards_list) >= 4:
                            break

                sub_entry = {
                    "title": sub.name,
                    "slug": sub.slug,
                    "url": getattr(sub, "get_absolute_url", lambda: "")(),
                    "columns": columns,
                    "items_flat": flat_items,
                    "cards": cards_list,
                }
                top_entry["children"].append(sub_entry)

            menu.append(top_entry)

        cache.set(cache_key, menu, 60 * 10)
    except Exception:
        logger.exception("Erreur build_menu_structure")
        return []

    return menu

def menu(request):
    """
    Context processor : expose 'menu' (structure Python) et 'menu_json' (JSON string) au template.
    """
    try:
        menu_data = build_menu_structure()
    except Exception:
        logger.exception("Impossible de construire le menu dans le context processor")
        menu_data = []

    try:
        menu_json = json.dumps(menu_data, ensure_ascii=False)
    except Exception:
        menu_json = "[]"

    return {"menu": menu_data, "menu_json": menu_json}


def cart_context(request):
    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    cart_count = 0
    for item in cart.values():
        try:
            cart_count += int(item.get("quantity", 0))
        except (TypeError, ValueError):
            pass

    return {
        "cart_count": cart_count
    }