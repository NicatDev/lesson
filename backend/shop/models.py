from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("ad", max_length=200)
    slug = models.SlugField("slug", max_length=220, unique=True, db_index=True)
    description = models.TextField("təsvir", blank=True)
    created_at = models.DateTimeField("yaradılıb", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "kateqoriya"
        verbose_name_plural = "kateqoriyalar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("ad", max_length=255)
    slug = models.SlugField(max_length=280, unique=True, db_index=True, blank=True)
    description = models.TextField("təsvir", blank=True)
    price = models.DecimalField("qiymət", max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField("ehtiyat", default=0)
    sku = models.CharField("SKU", max_length=64, unique=True, db_index=True)
    is_active = models.BooleanField("aktiv", default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="kateqoriya",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_products",
    )
    created_at = models.DateTimeField("yaradılıb", auto_now_add=True)
    updated_at = models.DateTimeField("yenilənib", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "məhsul"
        verbose_name_plural = "məhsullar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:200]
            self.slug = base or "mehsul"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
