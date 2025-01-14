from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='user_auth_app_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_auth_app_users', blank=True)

    def __str__(self):
        return self.username
