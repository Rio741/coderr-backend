from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from ...models import Order
from ..serializers.order_serializers import OrderSerializer
from ..permissions import IsOwnerOrReadOnly
from django.db import models
from rest_framework.exceptions import MethodNotAllowed


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            models.Q(customer_user=user) | models.Q(business_user=user)
        )

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Only admins can delete orders."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Blockiere PUT-Anfragen
        if not kwargs.get('partial', False):  # PUT hat `partial=False`
            raise MethodNotAllowed("PUT", detail="Full updates are not allowed. Use PATCH to update specific fields.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Explizite Behandlung für PATCH
        return super().partial_update(request, *args, **kwargs)