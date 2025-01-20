
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_hours = models.CharField(max_length=50, blank=True, null=True)
    file = models.ImageField(upload_to="profiles/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
