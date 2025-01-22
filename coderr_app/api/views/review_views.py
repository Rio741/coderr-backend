from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from ...models import Review
from ..serializers.review_serializers import ReviewSerializer
from ..permissions import IsOwnerOrAdmin
from rest_framework import serializers
from django.contrib.auth.models import User

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API-ViewSet für Bewertungen.
    
    - Ermöglicht das Erstellen, Abrufen, Aktualisieren und Löschen von Bewertungen.
    - Nutzer können nur ihre eigenen Bewertungen sehen und verwalten.
    - Nur Kunden dürfen Bewertungen erstellen.
    - Bewertungen dürfen nur für Geschäftsbenutzer abgegeben werden.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """Setzt die Berechtigungen basierend auf der Aktion."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Gibt nur Bewertungen zurück, die entweder vom Benutzer erstellt wurden oder sich auf ihn beziehen."""
        user = self.request.user
        if not user.is_authenticated:
            return Review.objects.none()
        return Review.objects.filter(
            reviewer=user
        ) | Review.objects.filter(
            business_user=user
        )

    def perform_create(self, serializer):
        """Erstellt eine neue Bewertung und stellt sicher, dass nur Kunden Geschäftsbenutzer bewerten können."""
        user = self.request.user

        if not user.userprofile.type == 'customer':
            raise permissions.PermissionDenied(
                "Only customers can create reviews.")

        business_user_id = self.request.data.get('business_user')
        business_user = get_object_or_404(User, id=business_user_id)

        if not business_user.userprofile.type == 'business':
            raise serializers.ValidationError(
                "You can only review business users.")

        serializer.save(reviewer=user, business_user=business_user)
