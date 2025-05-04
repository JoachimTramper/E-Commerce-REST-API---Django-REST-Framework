from rest_framework.pagination import PageNumberPagination


class FlexiblePageNumberPagination(PageNumberPagination):
    page_size = 10
    # Default page size for the client
    page_size_query_param = "page_size"
    max_page_size = 50
