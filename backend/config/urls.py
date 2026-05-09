from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from .views import SwaggerSwitchView

_AUTH_SCHEMA = {
    "TITLE": "Shop API — Autentifikasiya",
    "DESCRIPTION": "İctimai: qeydiyyat, giriş, token yeniləmə. Access token ömrü: 10 dəq.",
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SECURITY": [],
    "PREPROCESSING_HOOKS": ["config.schema_hooks.preprocess_auth_only"],
}

_SHOP_SCHEMA = {
    "TITLE": "Shop API — Kateqoriya və məhsullar",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
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
        RedirectView.as_view(url="/api/docs/?spec=auth", permanent=False),
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
        RedirectView.as_view(url="/api/docs/?spec=shop", permanent=False),
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
    path("api/docs/", SwaggerSwitchView.as_view(), name="swagger-ui"),
    path(
        "api/redoc/",
        RedirectView.as_view(url="/api/redoc/shop/", permanent=False),
        name="redoc-redirect",
    ),
    path("api/", include("shop.urls")),
]
