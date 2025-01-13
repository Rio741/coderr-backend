from rest_framework import viewsets, filters
from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from .filters import OfferFilter
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .filters import OfferFilter
from .pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.prefetch_related('details').select_related('user').distinct()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = OfferFilter
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        details_data = self.request.data.get('details', [])

        if len(details_data) != 3:
            raise ValidationError("Es müssen genau 3 Angebotsdetails angegeben werden.")
        
        offer_types = {detail['offer_type'] for detail in details_data}
        if offer_types != {'basic', 'standard', 'premium'}:
            raise ValidationError("Die Angebotsdetails müssen die Typen basic, standard und premium enthalten.")

        for detail in details_data:
            if not detail['features']:
                raise ValidationError("Jedes Angebotsdetail muss mindestens ein Feature enthalten.")
            if detail['delivery_time_in_days'] <= 0:
                raise ValidationError("Die Lieferzeit muss eine positive Zahl sein.")
            if detail['revisions'] < -1:
                raise ValidationError("Die Anzahl der Revisionen darf nicht kleiner als -1 sein (für unlimitierte Revisionen).")

        offer = serializer.save(user=self.request.user)
        offer_serializer = OfferSerializer(offer)
        return Response(offer_serializer.data)      

    

class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
