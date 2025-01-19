from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from ...models import Order
from user_auth_app.models import UserProfile

class OrderCountView(APIView):
    """
    Gibt die Anzahl der laufenden Bestellungen eines Geschäftsnutzers zurück.
    """
    def get(self, request, business_user_id):
        try:
            business_user = User.objects.get(id=business_user_id)
            # Überprüfen, ob der Benutzer ein Anbieter ist
            if not hasattr(business_user, 'userprofile') or business_user.userprofile.type != 'business':
                return Response({"error": "User is not a business provider."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        # Zähle Bestellungen mit Status "in_progress"
        count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    Gibt die Anzahl der abgeschlossenen Bestellungen eines Geschäftsnutzers zurück.
    """
    def get(self, request, business_user_id):
        try:
            business_user = User.objects.get(id=business_user_id)
            # Überprüfen, ob der Benutzer ein Anbieter ist
            if not hasattr(business_user, 'userprofile') or business_user.userprofile.type != 'business':
                return Response({"error": "User is not a business provider."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)

        # Zähle Bestellungen mit Status "completed"
        count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
