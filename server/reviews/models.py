from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from profiles.models import TouristProfile, GuideProfile
from tours.models import Tour
from bookings.models import Booking

class Review(models.Model):
    """
    Reviews and ratings for completed tours
    """
    # Relationships
    tourist = models.ForeignKey(
        TouristProfile,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    guide = models.ForeignKey(
        GuideProfile,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review'
    )
    
    # Review content
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Response from guide
    guide_response = models.TextField(blank=True)
    guide_responded_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        indexes = [
            models.Index(fields=['guide', 'rating']),
            models.Index(fields=['tour', 'rating']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_approved']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.tourist.user.username} for {self.guide.user.username} - {self.rating}★"
    
    def clean(self):
        """
        Validate that review is for a completed booking
        """
        if self.booking.status != 'completed':
            raise ValidationError({
                'booking': 'Can only review completed bookings.'
            })
        
        if self.booking.tourist != self.tourist:
            raise ValidationError({
                'tourist': 'Can only review your own bookings.'
            })
    
    def save(self, *args, **kwargs):
        self.clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update guide's average rating if this is a new review
        if is_new:
            self.update_guide_rating()
    
    def update_guide_rating(self):
        """
        Update guide's average rating and review count
        """
        from django.db.models import Avg, Count
        
        guide_stats = Review.objects.filter(
            guide=self.guide,
            is_approved=True
        ).aggregate(
            avg_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        
        self.guide.average_rating = guide_stats['avg_rating'] or 0
        self.guide.total_reviews = guide_stats['total_reviews'] or 0
        self.guide.save()
