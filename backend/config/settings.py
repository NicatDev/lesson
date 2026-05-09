from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-demo-change-in-production-use-env"

DEBUG = False

ALLOWED_HOSTS = ["178.104.92.41", "localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
    "users",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "az"

TIME_ZONE = "Asia/Baku"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Shop API",
    "DESCRIPTION": (
        "Swagger-də yuxarıdan **API sənədi** seçin (Auth / Shop). "
        "Shop əməliyyatları üçün **Authorize** ilə JWT daxil edin. "
        "Access token ömrü: **10 dəqiqə**."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
        "filter": True,
        "persistAuthorization": True,
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
        "docExpansion": "list",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
        "syntaxHighlight": {"theme": "agate"},
        "showExtensions": True,
        "showCommonExtensions": True,
    },
    "REDOC_UI_SETTINGS": {
        "hideDownloadButton": False,
        "expandResponses": "200,201",
        "pathInMiddlePanel": True,
        "nativeScrollbars": True,
    },
    "TAGS": [
        {"name": "Auth", "description": "İctimai: qeydiyyat, giriş, token yeniləmə."},
        {"name": "Kateqoriyalar", "description": "Kateqoriya siyahısı (JWT tələb olunur)."},
        {
            "name": "Məhsullar (sadə)",
            "description": "Yalnız kateqoriya filteri və created_at sıralaması (JWT).",
        },
        {
            "name": "Məhsullar (geniş)",
            "description": "Tam filter, sıralama, səhifələmə və məhsul yaratma (JWT).",
        },
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://178.104.92.41:324",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://178.104.92.41:324",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
