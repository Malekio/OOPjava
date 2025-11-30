from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for DZ-TourGuide platform
    """

    USER_TYPE_CHOICES = [
        ("tourist", "Tourist"),
        ("guide", "Guide"),
        ("admin", "Admin"),
    ]

    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="tourist"
    )
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["user_type"]),
            models.Index(fields=["is_verified"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.username} ({self.user_type})"

    def is_tourist(self):
        return self.user_type == "tourist"

    def is_guide(self):
        return self.user_type == "guide"

    @property
    def is_admin_user(self):
        return self.user_type == "admin" or self.is_superuser
