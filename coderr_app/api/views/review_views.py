from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ...models import Review
from ..serializers.review_serializers import ReviewSerializer
from ..permissions import IsOwnerOrAdmin
from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        
        # Überprüfen, ob der Benutzer ein Kundenprofil hat
        if not user.userprofile.type == 'customer':
            raise permissions.PermissionDenied("Only customers can create reviews.")

        # `business_user` aus den Request-Daten holen
        business_user_id = self.request.data.get('business_user')
        business_user = get_object_or_404(User, id=business_user_id)

        # Überprüfen, ob der `business_user` tatsächlich ein Geschäftsnutzer ist
        if not business_user.userprofile.type == 'business':
            raise serializers.ValidationError("You can only review business users.")

        # Speichern mit `business_user` und `reviewer`
        serializer.save(reviewer=user, business_user=business_user)
