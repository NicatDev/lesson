from rest_framework.pagination import PageNumberPagination


class SimpleProductPagination(PageNumberPagination):
    page_size = 15
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 50


class AdvancedProductPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 200
