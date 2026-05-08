from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter

from .filters import ProductAdvancedFilter
from .models import Category, Product
from .pagination import AdvancedProductPagination, SimpleProductPagination
from .serializers import (
    CategorySerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Kateqoriyalar siyahısı",
        tags=["Kateqoriyalar"],
        auth=[],
    ),
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


@extend_schema(
    summary="Sadə məhsul siyahısı",
    description=(
        "Yalnız **category** ilə filter; sıralama yalnız **created_at** və ya **-created_at**."
    ),
    tags=["Məhsullar (sadə)"],
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Kateqoriya ID",
            required=False,
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Yalnız `created_at` və ya `-created_at`",
            enum=["created_at", "-created_at"],
            required=False,
        ),
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
        OpenApiParameter(
            name="page_size",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
        ),
    ],
    auth=[],
)
class SimpleProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = SimpleProductPagination

    def get_queryset(self) -> QuerySet[Product]:
        qs = Product.objects.select_related("category").filter(is_active=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)
        ordering = self.request.query_params.get("ordering", "-created_at")
        if ordering not in ("created_at", "-created_at"):
            ordering = "-created_at"
        return qs.order_by(ordering)


@extend_schema_view(
    get=extend_schema(
        summary="Geniş filtr, sıralama və səhifələmə",
        description=(
            "Bütün əsas sahələr üzrə filter; **ordering** istənilən sahə üçün (məs: `price`, `-stock`). "
            "Səhifələmə: `page`, `page_size` (maks. 200)."
        ),
        tags=["Məhsullar (geniş)"],
        auth=[],
        parameters=[
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Çoxsütunlu: `price,-created_at`. Sahələr: id, name, slug, sku, price, stock, "
                    "is_active, category, created_by, created_at, updated_at"
                ),
                required=False,
            ),
        ],
    ),
    post=extend_schema(
        summary="Məhsul yarat",
        tags=["Məhsullar (geniş)"],
        request=ProductCreateSerializer,
        responses={201: ProductDetailSerializer},
    ),
)
class ProductAdvancedListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category").all()
    filterset_class = ProductAdvancedFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = (
        "id",
        "name",
        "slug",
        "sku",
        "price",
        "stock",
        "is_active",
        "category",
        "created_by",
        "created_at",
        "updated_at",
    )
    ordering = ["-created_at"]
    pagination_class = AdvancedProductPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductDetailSerializer
