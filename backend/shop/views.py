from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter

from config.schema_utils import RESP_400, RESP_401, RESP_403

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
        operation_id="categories_list",
        summary="Bütün kateqoriyalar",
        description=(
            "Aktiv məhsul təsnifatları üçün kateqoriya siyahısı. **JWT Bearer tələb olunur.**\n\n"
            "Səhifələmə yoxdur — bütün qeydlər bir cavabda qaytarılır (layihə miqyasında)."
        ),
        tags=["Kateqoriyalar"],
        responses={
            200: OpenApiResponse(
                response=CategorySerializer(many=True),
                description="Kateqoriya massivi.",
            ),
            401: RESP_401,
            403: RESP_403,
        },
        examples=[
            OpenApiExample(
                "Uğurlu cavab (qısa)",
                value=[
                    {
                        "id": 1,
                        "name": "Elektronika",
                        "slug": "elektronika",
                        "description": "…",
                        "created_at": "2026-05-08T12:00:00+04:00",
                    }
                ],
                response_only=True,
            ),
        ],
    ),
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None


@extend_schema_view(
    get=extend_schema(
        operation_id="products_list_simple",
        summary="Məhsullar — sadə API",
        description=(
            "**Məhdud filter:** yalnız `category` (ID). **Sıralama:** yalnız `created_at` və ya `-created_at`.\n\n"
            "Aktiv (`is_active=true`) məhsullar göstərilir. **JWT Bearer** mütləqdir.\n\n"
            "Səhifələmə: `page`, `page_size` (maks. 50)."
        ),
        tags=["Məhsullar (sadə)"],
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Kateqoriya **primary key** (məhdud filter).",
                required=False,
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="**Yalnız** `created_at` (köhnədən yeniyə) və ya `-created_at` (yenidən köhnəyə).",
                enum=["created_at", "-created_at"],
                required=False,
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Səhifə nömrəsi (1-dən).",
                required=False,
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Səhifə ölçüsü (maks. 50).",
                required=False,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=ProductListSerializer(many=True),
                description="Səhifələnmiş məhsul siyahısı (`count`, `next`, `previous`, `results`).",
            ),
            401: RESP_401,
            403: RESP_403,
        },
    ),
)
class SimpleProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (permissions.IsAuthenticated,)
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


_ADVANCED_FILTER_PARAMS = [
    OpenApiParameter(
        name="name",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Ad üzrə **icontains** axtarış.",
        required=False,
    ),
    OpenApiParameter(
        name="description",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Təsvir üzrə **icontains**.",
        required=False,
    ),
    OpenApiParameter(
        name="sku",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="SKU **icontains**.",
        required=False,
    ),
    OpenApiParameter(
        name="slug",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Slug **icontains**.",
        required=False,
    ),
    OpenApiParameter(
        name="price_min",
        type=OpenApiTypes.DECIMAL,
        location=OpenApiParameter.QUERY,
        description="Minimum qiymət (`price >=`).",
        required=False,
    ),
    OpenApiParameter(
        name="price_max",
        type=OpenApiTypes.DECIMAL,
        location=OpenApiParameter.QUERY,
        description="Maksimum qiymət (`price <=`).",
        required=False,
    ),
    OpenApiParameter(
        name="stock_min",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Minimum ehtiyat.",
        required=False,
    ),
    OpenApiParameter(
        name="stock_max",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Maksimum ehtiyat.",
        required=False,
    ),
    OpenApiParameter(
        name="created_after",
        type=OpenApiTypes.DATETIME,
        location=OpenApiParameter.QUERY,
        description="`created_at >=` (ISO 8601).",
        required=False,
    ),
    OpenApiParameter(
        name="created_before",
        type=OpenApiTypes.DATETIME,
        location=OpenApiParameter.QUERY,
        description="`created_at <=` (ISO 8601).",
        required=False,
    ),
    OpenApiParameter(
        name="updated_after",
        type=OpenApiTypes.DATETIME,
        location=OpenApiParameter.QUERY,
        description="`updated_at >=` (ISO 8601).",
        required=False,
    ),
    OpenApiParameter(
        name="updated_before",
        type=OpenApiTypes.DATETIME,
        location=OpenApiParameter.QUERY,
        description="`updated_at <=` (ISO 8601).",
        required=False,
    ),
    OpenApiParameter(
        name="category",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Kateqoriya ID (dəqiq uyğunluq).",
        required=False,
    ),
    OpenApiParameter(
        name="is_active",
        type=OpenApiTypes.BOOL,
        location=OpenApiParameter.QUERY,
        description="Aktiv məhsul filteri (`true` / `false`).",
        required=False,
    ),
    OpenApiParameter(
        name="created_by",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Yaradan istifadəçi ID.",
        required=False,
    ),
    OpenApiParameter(
        name="ordering",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description=(
            "Çoxsütunlu: `price,-created_at`. İcazəli sahələr: `id`, `name`, `slug`, `sku`, "
            "`price`, `stock`, `is_active`, `category`, `created_by`, `created_at`, `updated_at`. "
            "Azalan üçün sahə önünə `-` qoyun."
        ),
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
        description="Səhifə ölçüsü (maks. 200).",
        required=False,
    ),
]


@extend_schema_view(
    get=extend_schema(
        operation_id="products_list_advanced",
        summary="Məhsullar — geniş filter və sıralama",
        description=(
            "Bütün əsas **filter** parametrləri (ad, qiymət aralığı, tarix, kateqoriya, …) və "
            "**ordering** (istənilən icazəli sahə, asc/desc). **Səhifələmə:** `page`, `page_size` (maks. 200).\n\n"
            "**JWT Bearer** mütləqdir."
        ),
        tags=["Məhsullar (geniş)"],
        parameters=_ADVANCED_FILTER_PARAMS,
        responses={
            200: OpenApiResponse(
                response=ProductDetailSerializer(many=True),
                description="Səhifələnmiş nəticə; hər elementdə `description` daxildir.",
            ),
            401: RESP_401,
            403: RESP_403,
        },
    ),
    post=extend_schema(
        operation_id="products_create",
        summary="Yeni məhsul yarat",
        description=(
            "Autentifikasiya olunmuş istifadəçi adından məhsul yaradır (`created_by` avtomatik). "
            "`slug` boş qalsa, model tərəfindən avto doldurula bilər. **SKU** unikal olmalıdır.\n\n"
            "**JWT Bearer** mütləqdir."
        ),
        tags=["Məhsullar (geniş)"],
        request=ProductCreateSerializer,
        responses={
            201: ProductDetailSerializer,
            400: RESP_400,
            401: RESP_401,
            403: RESP_403,
        },
        examples=[
            OpenApiExample(
                "Nümunə məhsul",
                value={
                    "name": "Test məhsulu",
                    "slug": "",
                    "description": "Qısa təsvir",
                    "price": "29.99",
                    "stock": 100,
                    "sku": "SKU-TEST-001",
                    "is_active": True,
                    "category": 1,
                },
                request_only=True,
            ),
        ],
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
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductDetailSerializer
