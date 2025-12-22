# ecommerce/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
import random

# ---------------------------
# Classes existantes (Slider, Category, MenuColumn, MenuColumnItem, etc.)
# ---------------------------

class SliderImageManager(models.Manager):
    def get_slider_images(self, limit=5):
        """
        Retourne jusqu'à `limit` images:
        - si certaines ont selected=True -> retourne celles-ci (dans l'ordre DB).
        - sinon -> retourne `limit` images choisies aléatoirement sans charger tous les objets en mémoire.
        """
        selected_qs = self.filter(selected=True)
        if selected_qs.exists():
            return selected_qs[:limit]

        pks = list(self.values_list('pk', flat=True))
        if not pks:
            return self.none()
        if len(pks) <= limit:
            # peu d'images -> on retourne tout
            return self.filter(pk__in=pks)
        sampled = random.sample(pks, k=limit)
        return self.filter(pk__in=sampled)


class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider/')
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    selected = models.BooleanField(default=False)

    objects = SliderImageManager()

    def __str__(self):
        return self.title or f"Slider #{self.pk}"


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='category_thumbs/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_fixed = models.BooleanField(default=False, help_text="Garder visible dans la barre principale")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-is_fixed', 'order', 'name')

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validation pour empêcher :
        - parent = self (même instance ou même id)
        - cycles (remonter la chaîne de parents)
        """
        if self.parent is not None:
            if self.parent is self:
                raise ValidationError("Une catégorie ne peut pas être son propre parent.")
            if self.pk and self.parent_id == self.pk:
                raise ValidationError("Une catégorie ne peut pas être son propre parent.")

        ancestor = self.parent
        seen_ids = set()
        depth = 0
        while ancestor is not None:
            if ancestor is self:
                raise ValidationError("Cycle détecté : cette affectation ferait de la catégorie un descendant d'elle-même.")
            if ancestor.pk is not None:
                if ancestor.pk in seen_ids:
                    raise ValidationError("Cycle détecté dans la hiérarchie des catégories.")
                seen_ids.add(ancestor.pk)
            ancestor = ancestor.parent
            depth += 1
            if depth > 1000:
                raise ValidationError("Profondeur trop élevée dans la hiérarchie (possible cycle).")

    def _generate_unique_slug(self, value=None):
        base_value = value or self.name
        base = slugify(base_value)[:120] or 'category'
        slug = base
        i = 1
        qs = Category.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        orig = None
        if self.pk:
            try:
                orig = Category.objects.get(pk=self.pk)
            except Category.DoesNotExist:
                orig = None

        if not self.pk:
            if not self.slug:
                self.slug = self._generate_unique_slug()
        else:
            if orig and orig.name != self.name:
                new_slug = self._generate_unique_slug(self.name)
                if orig.slug and orig.slug != new_slug:
                    CategorySlugHistory.objects.create(category=self, old_slug=orig.slug)
                self.slug = new_slug

        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ecommerce:category_detail', kwargs={'slug': self.slug})


class CategorySlugHistory(models.Model):
    """
    Historique des anciens slugs pour redirection si besoin.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='slug_history')
    old_slug = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Historique slug catégorie"
        verbose_name_plural = "Historique slugs catégories"

    def __str__(self):
        return f"{self.old_slug} -> {self.category_id}"


class MenuColumn(models.Model):
    """
    Colonne de menu pour une sous-catégorie (niveau 2).
    """
    COLUMN_TYPE = [
        ('list', 'Liste'),
        ('brands', 'Marques'),
        ('cards', 'Cartes'),
    ]
    subcategory = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='menu_columns',
        help_text="La sous-catégorie (niveau 2) à laquelle cette colonne appartient."
    )
    order = models.PositiveSmallIntegerField(default=0)
    heading = models.CharField(max_length=120, blank=True)
    column_type = models.CharField(max_length=12, choices=COLUMN_TYPE, default='list')

    cards = models.ManyToManyField(
        Category, blank=True, related_name='menu_as_cards',
        help_text="(optionnel) catégories à afficher en vignettes (si vous utilisez encore ce champ)."
    )

    class Meta:
        ordering = ('order',)
        verbose_name = "Colonne de menu"
        verbose_name_plural = "Colonnes de menu"

    def __str__(self):
        return f"{self.subcategory.name} • {self.heading or self.get_column_type_display()}"

    def get_items(self):
        return Category.objects.filter(menu_items__menu_column=self).order_by('menu_items__order')


class MenuColumnItem(models.Model):
    """
    Liaison entre MenuColumn (colonne) et Category (niveau 3).
    Permet d'ajouter des métadonnées (order, is_card, visible...)
    """
    menu_column = models.ForeignKey(MenuColumn, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='menu_items')
    order = models.PositiveIntegerField(default=0)
    is_card = models.BooleanField(default=False, help_text="Afficher comme vignette si la colonne est de type 'cards'")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order',)
        unique_together = ('menu_column', 'category')

    def __str__(self):
        return f"{self.category} dans {self.menu_column} (ordre {self.order})"

    def clean(self):
        if self.category.parent_id != self.menu_column.subcategory_id:
            raise ValidationError("La colonne sélectionnée n'appartient pas à la même sous-catégorie que cette catégorie.")


# ---------------------------
# Nouveaux modèles produits / sections
# ---------------------------

class Brand(models.Model):
    """Marque simple pour les produits"""
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:120] or 'brand'
            slug = base
            i = 1
            qs = Brand.objects.all()
            while qs.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    """Produit principal"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=64, blank=True, null=True, help_text="Référence interne (SKU).")
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    primary_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    categories = models.ManyToManyField(Category, blank=True, related_name='products_extra')
    short_description = models.CharField(max_length=400, blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)

    price_current = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_original = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=8, default='USD')

    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)  # quantité disponible, si pertinent
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating_value = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    rating_count = models.PositiveIntegerField(default=0)

    seller = models.CharField(max_length=140, blank=True, null=True)
    is_promoted = models.BooleanField(default=False)
    promo_label = models.CharField(max_length=60, blank=True, null=True)

    # liaison vers sections via ProductSection (through)
    sections = models.ManyToManyField('Section', through='ProductSection', related_name='products')

    class Meta:
        ordering = ('-is_promoted', '-created_at', 'name')

    def __str__(self):
        return self.name

    def _generate_unique_slug(self, value=None):
        base_value = value or self.name
        base = slugify(base_value)[:240] or 'product'
        slug = base
        i = 1
        qs = Product.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        # génération du slug si absent
        if not self.slug:
            self.slug = self._generate_unique_slug()
        # validations (via clean)
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        # s'assurer que la primary_category est une feuille (pas d'enfants actifs)
        if self.primary_category and self.primary_category.children.filter(is_active=True).exists():
            raise ValidationError({'primary_category': "La catégorie principale doit être une catégorie feuille (sans sous-catégories actives)."})
        # coherent prices
        if self.price_original and self.price_current and self.price_original < self.price_current:
            # autoriser mais avertir : ici on laisse passer. Si tu veux empêcher, raise ValidationError.
            pass

    def get_absolute_url(self):
        return reverse('ecommerce:product_detail', kwargs={'slug': self.slug})

    def is_on_sale(self):
        return bool(self.price_original and self.price_current < self.price_original)

    def discount_percent(self):
        if not (self.price_original and self.price_original > 0):
            return 0
        try:
            return round((1 - (self.price_current / self.price_original)) * 100, 2)
        except Exception:
            return 0

    def current_price(self):
        return self.price_current


class ProductImage(models.Model):
    """Images liées au produit (une principale possible)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)
    def __str__(self):
        return f"Image {self.product} ({self.order})"


class Section(models.Model):
    """Sections globales du site (Accueil) - ex: Offres du jour, Tendances, Sponsorisé, Occasion"""
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:120] or 'section'
            slug = base
            i = 1
            qs = Section.objects.all()
            while qs.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductSection(models.Model):
    """
    Table intermédiaire product <-> section.
    Contient métadonnées : ordre, période, actif.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sections')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='product_sections')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order', '-created_at')
        unique_together = ('product', 'section')

    def __str__(self):
        return f"{self.product} ↦ {self.section} (ordre={self.order})"

    def is_current(self, when=None):
        now = when or timezone.now()
        if not self.is_active:
            return False
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True

# EOF

# Mettre en place l'etat des produits en favoris
from django.conf import settings

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ('-created_at',)
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"

    def __str__(self):
        return f"{self.user} ♥ {self.product}"

# Pour la preconfiguration

class ShopSettings(models.Model):
    shop_name = models.CharField(max_length=150)
    currency = models.CharField(max_length=10, default="USD")
    country = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to="shop/", blank=True, null=True)

    is_configured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paramètres boutique"
        verbose_name_plural = "Paramètres boutique"

    def __str__(self):
        return self.shop_name or "Shop settings"
