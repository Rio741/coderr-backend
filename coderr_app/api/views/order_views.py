from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ...models import Order
from ..serializers.order_serializers import OrderSerializer
from django.db import models
from rest_framework.exceptions import MethodNotAllowed

class OrderViewSet(viewsets.ModelViewSet):
    """
    API-ViewSet für Bestellungen.
    
    - Unterstützt das Erstellen, Abrufen, Aktualisieren und Löschen von Bestellungen.
    - Benutzer können nur ihre eigenen Bestellungen sehen.
    - Nur Admins können Bestellungen löschen.
    - Vollständige Updates (PUT) sind nicht erlaubt, nur partielle Updates (PATCH).
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Gibt nur die Bestellungen des authentifizierten Benutzers zurück."""
        user = self.request.user
        return Order.objects.filter(
            models.Q(customer_user=user) | models.Q(business_user=user)
        )

    def perform_create(self, serializer):
        """Setzt den `customer_user` automatisch auf den aktuell angemeldeten Benutzer."""
        serializer.save(customer_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Nur Admins dürfen Bestellungen löschen."""
        if not request.user.is_staff:
            return Response({"error": "Only admins can delete orders."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Verbietet vollständige Updates (PUT) und erlaubt nur partielle Updates (PATCH)."""
        if not kwargs.get('partial', False):
            raise MethodNotAllowed(
                "PUT", detail="Full updates are not allowed. Use PATCH to update specific fields.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Erlaubt partielle Updates für eine Bestellung."""
        return super().partial_update(request, *args, **kwargs)
