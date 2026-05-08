from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

_AUTH_SCHEMA = {
    "TITLE": "Shop API — Autentifikasiya",
    "DESCRIPTION": (
        "### İctimai endpointlər\n"
        "Bu sənəddə yalnız **qeydiyyat**, **giriş** və **token yeniləmə** var. "
        "**Authorize tələb olunmur.**\n\n"
        "- `POST /api/auth/register/` — yeni istifadəçi.\n"
        "- `POST /api/auth/token/` — `access` + `refresh` (access **10 dəq** etibarlıdır).\n"
        "- `POST /api/auth/token/refresh/` — yeni access (refresh göndərin).\n"
    ),
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SECURITY": [],
    "PREPROCESSING_HOOKS": ["config.schema_hooks.preprocess_auth_only"],
}

_SHOP_SCHEMA = {
    "TITLE": "Shop API — Kateqoriya və məhsullar",
    "DESCRIPTION": (
        "### Qorunan API\n"
        "Bütün əməliyyatlar üçün **JWT Bearer** tələb olunur.\n\n"
        "1. Əvvəl **Auth** Swagger-da və ya `POST /api/auth/token/` ilə token alın.\n"
        "2. Bu səhifədə yuxarıdan **Authorize** → `Bearer <access_token>` daxil edin.\n"
        "3. Access **10 dəqiqə** sonra bitə bilər — `refresh` ilə yeniləyin.\n\n"
        "**Sadə məhsul siyahısı** yalnız `category` + `ordering` (`created_at` / `-created_at`). "
        "**Geniş** endpoint bütün filter/sıralama/səhifələməni dəstəkləyir.\n"
    ),
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SECURITY": [{"bearerAuth": []}],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Access token (10 dəq).",
            }
        }
    },
    "PREPROCESSING_HOOKS": ["config.schema_hooks.preprocess_shop_only"],
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/schema/auth/",
        SpectacularAPIView.as_view(custom_settings=_AUTH_SCHEMA),
        name="schema-auth",
    ),
    path(
        "api/docs/auth/",
        SpectacularSwaggerView.as_view(url_name="schema-auth"),
        name="swagger-auth",
    ),
    path(
        "api/redoc/auth/",
        SpectacularRedocView.as_view(url_name="schema-auth"),
        name="redoc-auth",
    ),
    path(
        "api/schema/shop/",
        SpectacularAPIView.as_view(custom_settings=_SHOP_SCHEMA),
        name="schema-shop",
    ),
    path(
        "api/docs/shop/",
        SpectacularSwaggerView.as_view(url_name="schema-shop"),
        name="swagger-shop",
    ),
    path(
        "api/redoc/shop/",
        SpectacularRedocView.as_view(url_name="schema-shop"),
        name="redoc-shop",
    ),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(custom_settings=_SHOP_SCHEMA),
        name="schema",
    ),
    path(
        "api/docs/",
        RedirectView.as_view(url="/api/docs/shop/", permanent=False),
        name="swagger-ui-redirect",
    ),
    path(
        "api/redoc/",
        RedirectView.as_view(url="/api/redoc/shop/", permanent=False),
        name="redoc-redirect",
    ),
    path("api/", include("shop.urls")),
]
