from django.db import models
from profiles.models import TouristProfile, GuideProfile


class Conversation(models.Model):
    """
    Conversation between tourist and guide
    """

    tourist = models.ForeignKey(
        TouristProfile, on_delete=models.CASCADE, related_name="conversations"
    )
    guide = models.ForeignKey(
        GuideProfile, on_delete=models.CASCADE, related_name="conversations"
    )
    subject = models.CharField(max_length=200, default="Tour Inquiry")
    last_message_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversations"
        unique_together = ["tourist", "guide"]
        indexes = [
            models.Index(fields=["tourist", "last_message_at"]),
            models.Index(fields=["guide", "last_message_at"]),
        ]
        ordering = ["-last_message_at"]

    def __str__(self):
        return f"{self.tourist.user.username} <-> {self.guide.user.username}"


class Message(models.Model):
    """
    Messages within conversations
    """

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender_type = models.CharField(
        max_length=10, choices=[("tourist", "Tourist"), ("guide", "Guide")]
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
            models.Index(fields=["is_read"]),
        ]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender_type}: {self.content[:50]}..."


class CustomTourRequest(models.Model):
    """
    Custom tour requests from tourists
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    ]

    tourist = models.ForeignKey(
        TouristProfile, on_delete=models.CASCADE, related_name="custom_requests"
    )
    guide = models.ForeignKey(
        GuideProfile, on_delete=models.CASCADE, related_name="custom_requests"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Describe your ideal tour")
    preferred_date = models.DateField()
    duration_hours = models.PositiveIntegerField(
        help_text="Estimated duration in hours"
    )
    group_size = models.PositiveIntegerField(default=1)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    special_requirements = models.TextField(blank=True)

    # Guide response
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    guide_response = models.TextField(blank=True)
    proposed_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    alternative_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "custom_tour_requests"
        indexes = [
            models.Index(fields=["tourist", "status"]),
            models.Index(fields=["guide", "status"]),
            models.Index(fields=["preferred_date"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.title} - {self.tourist.user.username} to {self.guide.user.username}"
        )
