from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist

class AuthenticatedOwnerPermission(BasePermission):
    """
    Berechtigungsklasse für authentifizierte Besitzer.
    
    - Lesezugriff für alle Benutzer erlaubt.
    - Schreibzugriff nur für den Besitzer des Objekts oder einen Admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user or request.user.is_staff

class IsProvider(BasePermission):
    """
    Berechtigungsklasse für Anbieter.
    
    - Erlaubt Zugriff für authentifizierte Geschäftsbenutzer.
    - Admins und Superuser haben ebenfalls Zugriff.
    """
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
    """
    Berechtigungsklasse für Objekteigentümer oder schreibgeschützten Zugriff.
    
    - Lesezugriff für alle Benutzer erlaubt.
    - Schreibzugriff nur für den Besitzer der Bestellung (Kunde oder Anbieter).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.customer_user == request.user or obj.business_user == request.user

class IsAdminUserOrReadOnly(BasePermission):
    """
    Berechtigungsklasse für Administratoren oder schreibgeschützten Zugriff.
    
    - Lesezugriff für alle Benutzer erlaubt.
    - Schreibzugriff nur für Administratoren.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

class IsOwnerOrAdmin(BasePermission):
    """
    Berechtigungsklasse für Objekteigentümer oder Administratoren.
    
    - Schreibzugriff nur für den Ersteller der Bewertung oder einen Admin.
    """
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user or request.user.is_staff
