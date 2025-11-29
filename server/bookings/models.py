from django.db import models
from profiles.models import TouristProfile
from tours.models import Tour

class Booking(models.Model):
    """
    Simple tour booking system
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Relationships
    tourist = models.ForeignKey(
        TouristProfile,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Booking details
    booking_date = models.DateField()
    time_slot = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning (8:00-12:00)'),
            ('afternoon', 'Afternoon (13:00-17:00)'), 
            ('evening', 'Evening (18:00-22:00)'),
            ('full_day', 'Full Day (8:00-17:00)'),
        ],
        default='morning'
    )
    group_size = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Optional notes
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['booking_date']),
            models.Index(fields=['tourist']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.tour.title}"
    
    @property
    def guide(self):
        """Get the guide from the tour"""
        return self.tour.guide
    
    def save(self, *args, **kwargs):
        # Auto-calculate total price
        if not self.total_price:
            self.total_price = self.tour.price * self.group_size
        super().save(*args, **kwargs)
