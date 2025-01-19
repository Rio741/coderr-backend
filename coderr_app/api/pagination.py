from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 6  # Standard Page Size (Frontend sollte denselben Wert verwenden)
    page_size_query_param = 'page_size'  # Erlaubt dem Client, eine eigene `page_size` zu setzen
    max_page_size = 50  # Maximale Anzahl pro Seite
