from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from ...models import Order

class OrderCountView(APIView):
    """
    API-View zur Ermittlung der Anzahl an laufenden Bestellungen für einen Geschäftsanbieter.
    
    - Überprüft, ob der Benutzer existiert und ein Geschäftsprofil hat.
    - Gibt die Anzahl der Bestellungen mit dem Status `in_progress` zurück.
    """
    def get(self, request, business_user_id):
        """Ermittelt die Anzahl der laufenden Bestellungen für einen Geschäftsanbieter."""
        try:
            business_user = User.objects.get(id=business_user_id)
            if not hasattr(business_user, 'userprofile') or business_user.userprofile.type != 'business':
                return Response({"error": "User is not a business provider."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(
            business_user=business_user, status='in_progress').count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)

class CompletedOrderCountView(APIView):
    """
    API-View zur Ermittlung der Anzahl abgeschlossener Bestellungen für einen Geschäftsanbieter.
    
    - Überprüft, ob der Benutzer existiert und ein Geschäftsprofil hat.
    - Gibt die Anzahl der Bestellungen mit dem Status `completed` zurück.
    """
    def get(self, request, business_user_id):
        """Ermittelt die Anzahl der abgeschlossenen Bestellungen für einen Geschäftsanbieter."""
        try:
            business_user = User.objects.get(id=business_user_id)
            if not hasattr(business_user, 'userprofile') or business_user.userprofile.type != 'business':
                return Response({"error": "User is not a business provider."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        count = Order.objects.filter(
            business_user=business_user, status='completed').count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
