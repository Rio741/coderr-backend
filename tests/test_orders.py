from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from coderr_app.models import Order, Offer, OfferDetail
from user_auth_app.models import UserProfile

class OrderAPITestCase(APITestCase):

    def setUp(self):
        # Erstelle Benutzer
        self.customer_user = User.objects.create_user(username="customer", password="password")
        self.business_user = User.objects.create_user(username="business", password="password")

        # Erstelle UserProfile
        UserProfile.objects.create(user=self.customer_user, type="customer")
        UserProfile.objects.create(user=self.business_user, type="business")

        # Erstelle Angebot und Angebotsdetails
        self.offer = Offer.objects.create(user=self.business_user, title="Test Offer")
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Package",
            revisions=2,
            delivery_time_in_days=5,
            price=100.00,
            features=["Feature 1"],
            offer_type="basic"
        )

        # Authentifiziere Kunde
        self.client = APIClient()
        self.client.login(username="customer", password="password")

    def test_create_order(self):
        """Testet die Erstellung einer Bestellung."""
        response = self.client.post("/orders/", {"offer_detail_id": self.offer_detail.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.customer_user, self.customer_user)
        self.assertEqual(order.business_user, self.business_user)
        self.assertEqual(order.title, self.offer_detail.title)

    def test_get_orders(self):
        """Testet das Abrufen von Bestellungen."""
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Test Order",
            revisions=1,
            delivery_time_in_days=3,
            price=50.00,
            features=["Feature 1"],
            offer_type="basic",
        )
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_order_status(self):
        """Testet das Aktualisieren des Status einer Bestellung."""
        order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Test Order",
            revisions=1,
            delivery_time_in_days=3,
            price=50.00,
            features=["Feature 1"],
            offer_type="basic",
            status=Order.IN_PROGRESS,
        )
        response = self.client.patch(f"/orders/{order.id}/", {"status": Order.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.COMPLETED)

    def test_delete_order_as_admin(self):
        """Testet das Löschen einer Bestellung durch einen Admin."""
        order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Test Order",
            revisions=1,
            delivery_time_in_days=3,
            price=50.00,
            features=["Feature 1"],
            offer_type="basic",
        )
        # Admin-Benutzer erstellen und authentifizieren
        admin_user = User.objects.create_superuser(username="admin", password="password")
        self.client.login(username="admin", password="password")
        response = self.client.delete(f"/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_delete_order_as_non_admin(self):
        """Testet das Löschen einer Bestellung durch einen Nicht-Admin-Benutzer."""
        order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Test Order",
            revisions=1,
            delivery_time_in_days=3,
            price=50.00,
            features=["Feature 1"],
            offer_type="basic",
        )
        response = self.client.delete(f"/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Order.objects.count(), 1)
