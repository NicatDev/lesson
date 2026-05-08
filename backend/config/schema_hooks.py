"""drf-spectacular: sxemi iki hissəyə bölmək üçün preprocessing hook-lar."""


def _norm(path: str) -> str:
    return path if path.startswith("/") else f"/{path}"


def preprocess_auth_only(endpoints, **kwargs):
    """Yalnız /api/auth/* endpointləri (qeydiyyat, login, refresh)."""
    out = []
    for tup in endpoints:
        path = _norm(tup[0])
        if path.startswith("/api/auth/"):
            out.append(tup)
    return out


def preprocess_shop_only(endpoints, **kwargs):
    """Kateqoriya və məhsul API-ləri (/api/categories/, /api/products/)."""
    out = []
    for tup in endpoints:
        path = _norm(tup[0])
        if path.startswith("/api/categories/") or path.startswith("/api/products/"):
            out.append(tup)
    return out
