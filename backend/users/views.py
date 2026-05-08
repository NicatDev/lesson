from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.schema_utils import RESP_400

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        operation_id="auth_register",
        summary="İstifadəçi qeydiyyatı",
        description=(
            "Yeni hesab yaradır. **İctimai** endpoint — token tələb olunmur.\n\n"
            "**Növbəti addım:** `POST /api/auth/token/` ilə eyni `username` / `password` "
            "göndərib access və refresh token alın. Access token ömrü **10 dəqiqə**dir."
        ),
        tags=["Auth"],
        auth=[],
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                response=RegisterSerializer,
                description="Hesab yaradıldı.",
            ),
            400: RESP_400,
        },
        examples=[
            OpenApiExample(
                "Nümunə qeydiyyat",
                value={
                    "username": "demo_user",
                    "password": "demo12345",
                    "first_name": "Demo",
                    "last_name": "İstifadəçi",
                    "phone_number": "+994501112233",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        operation_id="auth_token_obtain",
        summary="Giriş — access və refresh token",
        description=(
            "Etibarlı `username` və `password` ilə **JWT** cütlüyü qaytarır.\n\n"
            "| Sahə | İzah |\n|------|------|\n| `access` | API sorğularında `Authorization: Bearer ...` (≈ **10 dəq**) |\n"
            "| `refresh` | Access bitəndə `/api/auth/token/refresh/` üçün |\n\n"
            "**İctimai** endpoint."
        ),
        tags=["Auth"],
        auth=[],
        responses={
            200: OpenApiResponse(
                description="Token cütlüyü",
                response={
                    "type": "object",
                    "required": ["access", "refresh"],
                    "properties": {
                        "access": {"type": "string", "description": "JWT access (10 dəq)"},
                        "refresh": {"type": "string", "description": "JWT refresh"},
                    },
                },
            ),
            400: RESP_400,
            401: OpenApiResponse(
                description="Yanlış istifadəçi adı və ya şifrə (etibarsız credential)."
            ),
        },
        examples=[
            OpenApiExample(
                "Admin (seed)",
                value={"username": "admin", "password": "123123"},
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        operation_id="auth_token_refresh",
        summary="Access token yenilə",
        description=(
            "Əvvəl alınmış **refresh** token ilə yeni **access** (və konfiqurasiyaya görə yeni refresh) alır.\n\n"
            "Access token ömrü **10 dəqiqə** olduğu üçün uzun sessiyalarda bu endpoint mütləqdir.\n\n"
            "**İctimai** endpoint — Bearer access tələb olunmur, yalnız gövdədə `refresh`."
        ),
        tags=["Auth"],
        auth=[],
        responses={
            200: OpenApiResponse(
                description="Yeni access (və bəzən refresh)",
                response={
                    "type": "object",
                    "properties": {
                        "access": {"type": "string"},
                        "refresh": {"type": "string"},
                    },
                },
            ),
            400: RESP_400,
            401: OpenApiResponse(
                description="Refresh token etibarsızdır, müddəti bitib və ya format səhvdir."
            ),
        },
        examples=[
            OpenApiExample(
                "Refresh göndər",
                value={"refresh": "<eyJ0eXAiOiJKV1QiLCJhbGc...>"},
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
