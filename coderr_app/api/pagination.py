from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 6  # Passe diesen Wert an
    page_size_query_param = 'page_size'

