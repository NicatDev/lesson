"""Swagger/OpenAPI üçün ümumi cavab təsvirləri."""

from drf_spectacular.utils import OpenApiResponse

RESP_400 = OpenApiResponse(
    description=(
        "Sorğu gövdəsi və ya parametrlər validasiyadan keçmədi. "
        "Cavabda sahə adları üzrə səhv siyahısı qaytarıla bilər."
    ),
)
RESP_401 = OpenApiResponse(
    description=(
        "JWT **Bearer** access token tələb olunur: `Authorization: Bearer <access>`. "
        "**Access token ömrü 10 dəqiqədir.** Bitəndə `/api/auth/token/refresh/` ilə "
        "yeni access (və konfiqurasiyadan asılı olaraq refresh) alın."
    ),
)
RESP_403 = OpenApiResponse(
    description="Autentifikasiya olunub, lakin bu resursa giriş üçün kifayət deyil."
)
RESP_404 = OpenApiResponse(description="Resurs tapılmadı.")
