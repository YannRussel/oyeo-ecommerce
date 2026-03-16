from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import (
    SliderImage, Category, CategorySlugHistory, MenuColumn, MenuColumnItem,
    Brand, Product, ProductImage, Section, ProductSection
)


# -------------------------
# AdminHelpMixin (affiche une aide lisible pour les non-tech)
# -------------------------
class AdminHelpMixin:
    """
    Mixin à ajouter aux ModelAdmin pour afficher une boîte d'aide en haut du formulaire d'édition.
    Définissez `admin_help` (HTML simple) sur la classe ModelAdmin.
    """
    change_form_template = "admin/custom_change_form.html"
    admin_help = ""  # override dans chaque ModelAdmin si besoin

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['admin_help'] = mark_safe(getattr(self, 'admin_help', ''))
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)


# -------------------------
# Inlines utiles
# -------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_main', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    ordering = ('order',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:80px; object-fit:contain;"/>', obj.image.url)
        return "-"
    image_preview.short_description = _("Aperçu")


class ProductSectionInline(admin.TabularInline):
    model = ProductSection
    extra = 0
    fields = ('section', 'order', 'is_active', 'start_date', 'end_date', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


class CategorySlugHistoryInline(admin.TabularInline):
    model = CategorySlugHistory
    extra = 0
    readonly_fields = ('old_slug', 'created_at')
    can_delete = False
    verbose_name = _("Ancien slug")
    verbose_name_plural = _("Historique des slugs")


# -------------------------
# Category admin
# -------------------------
@admin.register(Category)
class CategoryAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Catégorie</h3>
    <ul>
      <li><strong>Créer</strong> : cliquez sur <em>Ajouter</em>, remplissez <em>Nom</em> — le slug est généré automatiquement.</li>
      <li><strong>Parent</strong> : si cette catégorie appartient à une catégorie plus large, sélectionnez-la ici. Pour une catégorie "feuille" (où l'on ajoute des produits), ne mettez pas d'enfant actif dessous.</li>
      <li><strong>Thumbnail</strong> : téléversez une image pour la vignette de la catégorie.</li>
      <li><strong>Activer / Désactiver</strong> : décochez <em>is_active</em> pour masquer la catégorie sur le site.</li>
      <li>Si vous voulez changer l'ordre, utilisez les actions <em>Déplacer vers le haut</em> / <em>Déplacer vers le bas</em>.</li>
    </ul>
    <p>Contact support si vous n'êtes pas sûr : <em>nom@ton-site.tld</em></p>
    """

    list_display = ('name', 'parent', 'is_active', 'is_fixed', 'order', 'thumbnail_preview')
    list_filter = ('is_active', 'is_fixed')
    search_fields = ('name', 'slug')
    ordering = ('-is_fixed', 'order', 'name')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('parent',)
    inlines = (CategorySlugHistoryInline,)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'description', 'thumbnail')
        }),
        ('Affichage & options', {
            'fields': ('is_active', 'is_fixed', 'order')
        }),
    )
    actions = ('make_active', 'make_inactive', 'move_up', 'move_down')

    def thumbnail_preview(self, obj):
        if obj and obj.thumbnail:
            return format_html('<img src="{}" style="height:60px; object-fit:cover; border-radius:4px;" />', obj.thumbnail.url)
        return "-"
    thumbnail_preview.short_description = _("Vignette")

    @admin.action(description="Marquer sélectionnées comme actives")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} catégorie(s) activée(s).")

    @admin.action(description="Marquer sélectionnées comme inactives")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} catégorie(s) désactivée(s).")

    @admin.action(description="Déplacer vers le haut (réduit l'order)")
    def move_up(self, request, queryset):
        for obj in queryset:
            if obj.order > 0:
                obj.order = max(0, obj.order - 1)
                obj.save()
        self.message_user(request, "Déplacé vers le haut.")

    @admin.action(description="Déplacer vers le bas (augmente l'order)")
    def move_down(self, request, queryset):
        for obj in queryset:
            obj.order = obj.order + 1
            obj.save()
        self.message_user(request, "Déplacé vers le bas.")


# -------------------------
# Brand admin
# -------------------------
@admin.register(Brand)
class BrandAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Marque</h3>
    <ul>
      <li>Ajoutez le nom de la marque. Le slug sera généré automatiquement.</li>
      <li>Téléversez un logo si vous en avez.</li>
    </ul>
    """

    list_display = ('name', 'logo_preview')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html('<img src="{}" style="height:40px; object-fit:contain;"/>', obj.logo.url)
        return "-"
    logo_preview.short_description = _("Logo")


# -------------------------
# Product admin
# -------------------------
@admin.register(Product)
class ProductAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Produit</h3>
    <p>Avant de créer un produit, créez d'abord sa <strong>catégorie feuille</strong> (ex: Vêtements > Robes).</p>
    <ol>
      <li><strong>Nom</strong> : donnez un nom clair.</li>
      <li><strong>Primary category</strong> : sélectionner la catégorie <em>feuille</em> (OBLIGATOIRE).</li>
      <li><strong>Images</strong> : ajoutez au moins une image puis cochez <em>is_main</em> sur l'image principale (inline "Images").</li>
      <li><strong>Prix</strong> : renseignez <em>price_current</em>. Si promo, remplissez <em>price_original</em> et <em>promo_label</em>.</li>
      <li><strong>Sections</strong> : liez à une section via l'inline <em>ProductSection</em> pour mettre en avant le produit.</li>
      <li>Enregistrer. Si un message d'erreur apparaît, lisez-le (il explique quoi corriger).</li>
    </ol>
    <p>Besoin d'aide ? Contact : <em>nom@ton-site.tld</em></p>
    """

    list_display = ('name', 'sku', 'brand_link', 'primary_category', 'price_current', 'stock', 'is_active', 'is_promoted', 'created_at')
    list_editable = ('price_current', 'stock', 'is_active', 'is_promoted')
    list_filter = ('is_active', 'is_promoted', 'brand', 'primary_category')
    search_fields = ('name', 'sku', 'brand__name')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ProductImageInline, ProductSectionInline)
    filter_horizontal = ('categories',)
    autocomplete_fields = ('brand', 'primary_category')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'sku', 'brand', 'primary_category', 'categories', 'short_description', 'long_description')
        }),
        ('Prix & stock', {
            'fields': ('price_current', 'price_original', 'currency', 'stock')
        }),
        ('Promotions & vendeur', {
            'fields': ('is_promoted', 'promo_label', 'seller')
        }),
        ('Options & meta', {
            'fields': ('is_active', 'rating_value', 'rating_count')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def brand_link(self, obj):
        if obj.brand:
            url = reverse('admin:ecommerce_brand_change', args=[obj.brand.pk])
            return format_html('<a href="{}">{}</a>', url, obj.brand.name)
        return "-"
    brand_link.short_description = _("Marque")

    @admin.action(description="Marquer comme promu")
    def mark_promoted(self, request, queryset):
        updated = queryset.update(is_promoted=True)
        self.message_user(request, f"{updated} produit(s) marqué(s) promu.")

    @admin.action(description="Retirer promotion")
    def unpromote(self, request, queryset):
        updated = queryset.update(is_promoted=False)
        self.message_user(request, f"{updated} produit(s) non promu.")


# -------------------------
# ProductSection admin
# -------------------------
@admin.register(ProductSection)
class ProductSectionAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Liaison Produit ↔ Section</h3>
    <ul>
      <li>Utilisez cette interface si vous voulez afficher un produit dans une Section (ex: A la une).</li>
      <li>Renseignez <em>start_date</em> et <em>end_date</em> pour définir la période d'affichage.</li>
    </ul>
    """

    list_display = ('product', 'section', 'order', 'is_active', 'start_date', 'end_date', 'created_at')
    list_filter = ('is_active', 'section')
    search_fields = ('product__name', 'section__name')
    raw_id_fields = ('product', 'section')
    ordering = ('section', 'order', '-created_at')


# -------------------------
# Section admin
# -------------------------
@admin.register(Section)
class SectionAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Section (ex: A la une)</h3>
    <p>Les sections sont des emplacements sur le site (Accueil, Offres). Liez des produits via ProductSection.</p>
    """

    list_display = ('name', 'slug', 'is_active', 'order')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# -------------------------
# SliderImage admin
# -------------------------
@admin.register(SliderImage)
class SliderImageAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Image du slider</h3>
    <ul>
      <li>Téléversez l'image et ajoutez un titre.</li>
      <li>Cochez <em>selected</em> pour prioriser cette image dans le slider.</li>
    </ul>
    """

    list_display = ('__str__', 'selected', 'image_preview')
    list_editable = ('selected',)
    search_fields = ('title',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:80px; object-fit:cover;"/>', obj.image.url)
        return "-"
    image_preview.short_description = _("Aperçu")


# -------------------------
# MenuColumn / MenuColumnItem admin
# -------------------------
@admin.register(MenuColumn)
class MenuColumnAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Colonne de menu</h3>
    <p>Gère l'affichage des sous-catégories dans le menu.</p>
    """

    list_display = ('subcategory', 'heading', 'column_type', 'order')
    search_fields = ('heading', 'subcategory__name')
    inlines = ()


@admin.register(MenuColumnItem)
class MenuColumnItemAdmin(AdminHelpMixin, admin.ModelAdmin):
    admin_help = """
    <h3>Guide rapide — Élément de colonne de menu</h3>
    <p>Relie une catégorie (niveau 3) à une colonne de menu.</p>
    """

    list_display = ('menu_column', 'category', 'order', 'is_card', 'is_active')
    list_filter = ('is_card', 'is_active')
    raw_id_fields = ('menu_column', 'category')

