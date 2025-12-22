# ecommerce/cache_utils.py
from django.core.cache import cache

SECTION_CACHE_KEY = "section_products_v1:{}"  # format with slug

def set_section_cache(slug, data, ttl=60):
    cache.set(SECTION_CACHE_KEY.format(slug), data, ttl)

def get_section_cache(slug):
    return cache.get(SECTION_CACHE_KEY.format(slug))

def delete_section_cache(slug):
    cache.delete(SECTION_CACHE_KEY.format(slug))
