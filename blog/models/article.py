from django.db import models
from django.conf import settings

from .category import Category


class Article(models.Model):
    PENDING = 'pending'
    VERIFIED = 'verified'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (VERIFIED, 'Verified'),
        (REJECTED, 'Rejected'),
    ]

    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLDEN = 'golden'

    SCOPE_CHOICES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLDEN, 'Golden'),
    ]

    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=50, default=PENDING)
    scope = models.CharField(choices=SCOPE_CHOICES,
                             max_length=50, default=BRONZE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
