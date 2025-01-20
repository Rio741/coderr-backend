from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from ...models import Review
from ..serializers.review_serializers import ReviewSerializer
from ..permissions import IsOwnerOrAdmin
from rest_framework import serializers
from django.contrib.auth.models import User


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Review.objects.none()

        return Review.objects.filter(
            reviewer=user
        ) | Review.objects.filter(
            business_user=user
        )

    def perform_create(self, serializer):
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
