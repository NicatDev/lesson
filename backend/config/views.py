"""Swagger UI (sxem seçicisi ilə)."""

from django.middleware.csrf import get_token
from django.urls import reverse
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.response import Response


class SwaggerSwitchView(SpectacularSwaggerView):
    """Auth / Shop OpenAPI sxemlərini bir səhifədə select ilə dəyişdirir."""

    template_name = "swagger_ui_switch.html"

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                "title": "Shop API — sənədlər",
                "swagger_ui_css": self._swagger_ui_resource("swagger-ui.css"),
                "swagger_ui_bundle": self._swagger_ui_resource("swagger-ui-bundle.js"),
                "swagger_ui_standalone": self._swagger_ui_resource("swagger-ui-standalone-preset.js"),
                "favicon_href": self._swagger_ui_favicon(),
                # Nisbətən yol: brauzer həmişə cari origin (:324) ilə sorğu göndərir.
                # $host (portsu olmadan) + build_absolute_uri bəzən :80 URL yaradır → CORS.
                "schema_url_shop": reverse("schema-shop"),
                "schema_url_auth": reverse("schema-auth"),
                "settings": self._dump(spectacular_settings.SWAGGER_UI_SETTINGS),
                "oauth2_config": self._dump(spectacular_settings.SWAGGER_UI_OAUTH2_CONFIG),
                "csrf_header_name": self._get_csrf_header_name(),
                "csrf_token": get_token(request),
                "schema_auth_names": self._dump(self._get_schema_auth_names()),
            },
            template_name=self.template_name,
            headers={
                "Cross-Origin-Opener-Policy": "unsafe-none",
            },
        )
