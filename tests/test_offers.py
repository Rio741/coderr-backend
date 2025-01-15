from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from coderr_app.models import Offer, OfferDetail
from user_auth_app.models import UserProfile

User = get_user_model()


class OfferModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="securepassword"
        )
        self.offer = Offer.objects.create(
            user=self.user,
            title="Test Offer",
            description="Test Description",
        )

    def test_offer_creation(self):
        """Test that an Offer is created with correct fields."""
        self.assertEqual(self.offer.title, "Test Offer")
        self.assertEqual(self.offer.description, "Test Description")
        self.assertEqual(self.offer.user, self.user)

    def test_offer_str_representation(self):
        """Test the string representation of an Offer."""
        self.assertEqual(str(self.offer), "Test Offer")


class OfferDetailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="securepassword"
        )
        self.offer = Offer.objects.create(
            user=self.user,
            title="Test Offer",
            description="Test Description",
        )
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Package",
            revisions=2,
            delivery_time_in_days=5,
            price=49.99,
            offer_type=OfferDetail.BASIC,
        )

    def test_offer_detail_creation(self):
        """Test that an OfferDetail is created correctly."""
        self.assertEqual(self.offer_detail.title, "Basic Package")
        self.assertEqual(self.offer_detail.price, 49.99)
        self.assertEqual(self.offer_detail.offer, self.offer)

    def test_offer_detail_str_representation(self):
        """Test the string representation of an OfferDetail."""
        self.assertEqual(str(self.offer_detail), "Test Offer - basic")


class OfferAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="securepassword"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            type="business",
            is_provider=True  # Hier setzen wir is_provider auf True
        )
        self.client.login(username="testuser", password="securepassword")
        self.offer = Offer.objects.create(
            user=self.user,
            title="Test Offer",
            description="Test Description",
        )


    def test_create_offer(self):
        """Test creating an Offer with details."""
        url = "/api/offers/"
        data = {
            "title": "New Offer",
            "description": "New Description",
            "details": [
                {
                    "title": "Basic",
                    "price": 10.0,
                    "offer_type": "basic",
                    "delivery_time_in_days": 3,
                    "revisions": 1,
                    "features": ["Feature1"],
                },
                {
                    "title": "Standard",
                    "price": 20.0,
                    "offer_type": "standard",
                    "delivery_time_in_days": 5,
                    "revisions": 2,
                    "features": ["Feature2"],
                },
                {
                    "title": "Premium",
                    "price": 30.0,
                    "offer_type": "premium",
                    "delivery_time_in_days": 7,
                    "revisions": 3,
                    "features": ["Feature3"],
                },
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["details"]), 3)