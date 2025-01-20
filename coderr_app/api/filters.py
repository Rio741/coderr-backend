import django_filters
from ..models import Offer
from django.db.models import Q


class OfferFilter(django_filters.FilterSet):
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
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
