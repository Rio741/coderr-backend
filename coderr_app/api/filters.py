import django_filters
from ..models import Offer
from django.db.models import Q

class OfferFilter(django_filters.FilterSet):
    """
    Filterklasse für Angebote.
    
    - Ermöglicht das Filtern nach Ersteller-ID, Mindestpreis und maximaler Lieferzeit.
    - Bietet eine Suchfunktion für Titel und Beschreibung.
    - Unterstützt Sortierung nach Aktualisierungsdatum und Preis.
    """
    creator_id = django_filters.NumberFilter(
        field_name='user__id', label='Creator ID')
    min_price = django_filters.NumberFilter(
        field_name='details__price', lookup_expr='gte', label='Min Price')
    max_delivery_time = django_filters.NumberFilter(
        field_name='details__delivery_time_in_days', lookup_expr='lte', label='Max Delivery Time')
    search = django_filters.CharFilter(method='filter_search', label='Search')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('updated_at', 'updated_at'),
            ('details__price', 'min_price'),
        ),
        label='Ordering',
    )

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']

    def filter_search(self, queryset, name, value):
        """Filtert Angebote basierend auf einer Suchanfrage in Titel oder Beschreibung."""
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
