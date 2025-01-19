from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from ...models import Offer, Review
from user_auth_app.models import UserProfile
from rest_framework.permissions import AllowAny

class BaseInfoView(APIView):
    permission_classes = [AllowAny] 
    """
    Gibt allgemeine Basisinformationen zur Plattform zurück.
    """
    def get(self, request):
        # Anzahl der Bewertungen
        review_count = Review.objects.count()

        # Durchschnittliches Bewertungsergebnis
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating')).get('avg_rating', 0)
        average_rating = round(average_rating or 0, 1)  # Runde auf eine Dezimalstelle

        # Anzahl der Geschäftsnutzer
        business_profile_count = UserProfile.objects.filter(type='business').count()

        # Anzahl der Angebote
        offer_count = Offer.objects.count()

        # Antwort zusammenstellen
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)
