from django.urls import path

from users.views import LoginView, RefreshView, RegisterView

from .views import CategoryListView, ProductAdvancedListCreateView, SimpleProductListView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/simple/", SimpleProductListView.as_view(), name="product-list-simple"),
    path("products/", ProductAdvancedListCreateView.as_view(), name="product-list-advanced"),
]
