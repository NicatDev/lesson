import django_filters

from .models import Category, Product


class CategoryFilter(django_filters.FilterSet):
    """Kateqoriya siyahısı üçün dəqiq filter parametrləri (Swagger ilə uyğun)."""

    id = django_filters.NumberFilter()
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    slug = django_filters.CharFilter(field_name="slug", lookup_expr="icontains")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Category
        fields = []


class ProductAdvancedFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    description = django_filters.CharFilter(field_name="description", lookup_expr="icontains")
    sku = django_filters.CharFilter(field_name="sku", lookup_expr="icontains")
    slug = django_filters.CharFilter(field_name="slug", lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stock_min = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    stock_max = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")
    updated_after = django_filters.IsoDateTimeFilter(field_name="updated_at", lookup_expr="gte")
    updated_before = django_filters.IsoDateTimeFilter(field_name="updated_at", lookup_expr="lte")

    class Meta:
        model = Product
        fields = {
            "category": ["exact"],
            "is_active": ["exact"],
            "created_by": ["exact"],
        }
