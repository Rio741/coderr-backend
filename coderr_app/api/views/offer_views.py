from rest_framework import viewsets, filters
from ...models import Offer, OfferDetail
from ..serializers.offer_serializers import OfferListSerializer, OfferDetailViewSerializer, OfferDetailSerializer, OfferCreateSerializer
from ..filters import OfferFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..pagination import CustomPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from ..permissions import AuthenticatedOwnerPermission, IsProvider
from rest_framework import status


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.prefetch_related("details").select_related("user").distinct()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = OfferFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Wechselt zwischen Serializern basierend auf der Aktion."""
        if self.action in ["retrieve", "update", "partial_update"]:  
            return OfferDetailViewSerializer
        elif self.action == "create":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsProvider]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [AuthenticatedOwnerPermission]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        details_data = self.request.data.get("details", [])

        if len(details_data) != 3:
            raise ValidationError(
                "Es müssen genau 3 Angebotsdetails angegeben werden.")

        offer_types = {detail["offer_type"] for detail in details_data}
        if offer_types != {"basic", "standard", "premium"}:
            raise ValidationError(
                "Die Angebotsdetails müssen die Typen basic, standard und premium enthalten.")

        for detail in details_data:
            if not detail["features"]:
                raise ValidationError(
                    "Jedes Angebotsdetail muss mindestens ein Feature enthalten.")
            if int(detail["delivery_time_in_days"]) <= 0:
                raise ValidationError(
                    "Die Lieferzeit muss eine positive Zahl sein.")
            if int(detail["revisions"]) < -1:
                raise ValidationError(
                    "Die Anzahl der Revisionen darf nicht kleiner als -1 sein (für unlimitierte Revisionen).")

        offer = serializer.save(user=self.request.user)
        offer_serializer = OfferDetailViewSerializer(offer)
        return Response(offer_serializer.data)


class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [AuthenticatedOwnerPermission |
                          IsProvider | IsAuthenticatedOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        """Falls kein OfferDetail existiert, gebe eine leere 200-Response zurück."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except:
            return Response({}, status=status.HTTP_200_OK)