from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist


class AuthenticatedOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user or request.user.is_staff


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True

        try:
            return request.user.userprofile.type == 'business'
        except ObjectDoesNotExist:
            return False


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.customer_user == request.user or obj.business_user == request.user


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user or request.user.is_staff
