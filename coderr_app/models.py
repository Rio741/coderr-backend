from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Offer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    BASIC = 'basic'
    STANDARD = 'standard'
    PREMIUM = 'premium'

    OFFER_TYPES = [
        (BASIC, 'Basic'),
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
    ]

    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(null=True, blank=True)
    delivery_time_in_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default=BASIC)

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"




class Order(models.Model):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_orders'
    )
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_orders'
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OfferDetail.OFFER_TYPES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.title}"
    

class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    rating = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')  # Ein Benutzer kann pro Geschäftsnutzer nur eine Bewertung abgeben.

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username} - {self.rating}"