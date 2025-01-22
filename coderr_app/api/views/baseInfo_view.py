from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from ...models import Offer, Review
from user_auth_app.models import UserProfile
from rest_framework.permissions import AllowAny


class BaseInfoView(APIView):
    """
    API-Endpoint zur Bereitstellung allgemeiner Statistikdaten über die Plattform.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Holt allgemeine Plattform-Statistiken und gibt sie als JSON-Response zurück.
        
        Rückgabe:
        - `review_count`: Gesamtanzahl der Bewertungen.
        - `average_rating`: Durchschnittliche Bewertung (gerundet auf eine Dezimalstelle).
        - `business_profile_count`: Anzahl der Geschäftsprofile.
        - `offer_count`: Anzahl der Angebote auf der Plattform.
        """
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(
            avg_rating=Avg('rating')).get('avg_rating', 0)
        average_rating = round(average_rating or 0, 1)
        business_profile_count = UserProfile.objects.filter(
            type='business').count()
        offer_count = Offer.objects.count()
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)
