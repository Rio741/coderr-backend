from django.test import TestCase
from django.contrib.auth.models import User
from .models import Offer, OfferDetail, Order, Review
from django.test import TestCase

class OfferModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_create_offer(self):
        offer = Offer.objects.create(user=self.user, title="Test Offer", description="This is a test offer")
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(offer.title, "Test Offer")

    def test_offer_str_representation(self):
        offer = Offer.objects.create(user=self.user, title="Test Offer", description="This is a test offer")
        self.assertEqual(str(offer), "Test Offer")

    def test_offer_details_relation(self):
        offer = Offer.objects.create(user=self.user, title="Test Offer", description="Test offer description")
        detail = OfferDetail.objects.create(
            offer=offer,
            title="Basic Plan",
            revisions=2,
            delivery_time_in_days=5,
            price=99.99,
            offer_type=OfferDetail.BASIC
        )
        self.assertEqual(offer.details.count(), 1)
        self.assertEqual(offer.details.first().title, "Basic Plan")

    def test_offer_update(self):
        offer = Offer.objects.create(user=self.user, title="Initial Title", description="Initial Description")
        offer.title = "Updated Title"
        offer.save()
        self.assertEqual(Offer.objects.get(id=offer.id).title, "Updated Title")

    def test_offer_delete(self):
        offer = Offer.objects.create(user=self.user, title="Test Offer", description="Test offer description")
        offer_id = offer.id
        offer.delete()
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())



class OrderModelTests(TestCase):
    def setUp(self):
        self.customer_user = User.objects.create_user(username="customer", password="password")
        self.business_user = User.objects.create_user(username="business", password="password")
        self.offer = Offer.objects.create(user=self.business_user, title="Test Offer", description="Test Description")
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Plan",
            revisions=2,
            delivery_time_in_days=5,
            price=99.99,
            offer_type=OfferDetail.BASIC
        )

    def test_create_order(self):
        order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_detail.title,
            revisions=self.offer_detail.revisions,
            delivery_time_in_days=self.offer_detail.delivery_time_in_days,
            price=self.offer_detail.price,
            features=self.offer_detail.features,
            offer_type=self.offer_detail.offer_type
        )
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.customer_user, self.customer_user)
        self.assertEqual(order.business_user, self.business_user)

    def test_order_str_representation(self):
        order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_detail.title,
            revisions=self.offer_detail.revisions,
            delivery_time_in_days=self.offer_detail.delivery_time_in_days,
            price=self.offer_detail.price,
            features=self.offer_detail.features,
            offer_type=self.offer_detail.offer_type
        )
        self.assertEqual(str(order), f"Order #{order.id} - {order.title}")

    def test_order_delete(self):
        order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_detail.title,
            revisions=self.offer_detail.revisions,
            delivery_time_in_days=self.offer_detail.delivery_time_in_days,
            price=self.offer_detail.price,
            features=self.offer_detail.features,
            offer_type=self.offer_detail.offer_type
        )
        order_id = order.id
        order.delete()
        self.assertFalse(Order.objects.filter(id=order_id).exists())


class ReviewModelTests(TestCase):
    def setUp(self):
        self.customer_user = User.objects.create_user(username="customer", password="password")
        self.business_user = User.objects.create_user(username="business", password="password")

    def test_create_review(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description="Excellent service!"
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.business_user, self.business_user)
        self.assertEqual(review.reviewer, self.customer_user)
        self.assertEqual(review.rating, 5)

    def test_review_str_representation(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Good service!"
        )
        self.assertEqual(str(review), f"Review by {self.customer_user.username} for {self.business_user.username} - {review.rating}")

    def test_review_delete(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=3,
            description="Average service."
        )
        review_id = review.id
        review.delete()
        self.assertFalse(Review.objects.filter(id=review_id).exists())
