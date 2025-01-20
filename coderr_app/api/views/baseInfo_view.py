from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from ...models import Offer, Review
from user_auth_app.models import UserProfile
from rest_framework.permissions import AllowAny


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
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
