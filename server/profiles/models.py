from django.db import models
from django.conf import settings
from locations.models import Wilaya
from decimal import Decimal

class TouristProfile(models.Model):
    """
    Tourist profile with preferences and personal information
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='tourist_profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    preferred_language = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='tourists/profiles/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tourist_profiles'
    
    def __str__(self):
        return f"Tourist: {self.user.username}"

class GuideProfile(models.Model):
    """
    Guide profile with certifications, pricing, and coverage areas
    """
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='guide_profile'
    )
    bio = models.TextField(max_length=1000)
    profile_picture = models.ImageField(upload_to='guides/profiles/')
    years_of_experience = models.PositiveIntegerField(default=0)
    languages = models.JSONField(default=list)  # List of languages spoken
    coverage_areas = models.ManyToManyField(Wilaya, related_name='guides')
    
    # Pricing structure (Flexible Tariff Grid)
    half_day_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price for tours up to 4 hours"
    )
    full_day_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price for tours 4-8 hours"
    )
    extra_hour_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price per hour beyond 8 hours"
    )
    
    # Verification
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )
    verification_notes = models.TextField(blank=True)
    
    # Ratings
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    total_reviews = models.PositiveIntegerField(default=0)
    total_tours_completed = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'guide_profiles'
        indexes = [
            models.Index(fields=['verification_status']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Guide: {self.user.username}"
    
    @property
    def is_verified(self):
        return self.verification_status == 'verified'
    
    def calculate_tour_price(self, duration_hours):
        """
        Calculate tour price based on duration and pricing structure
        """
        if duration_hours <= 4:
            return self.half_day_price
        elif duration_hours <= 8:
            return self.full_day_price
        else:
            extra_hours = duration_hours - 8
            return self.full_day_price + (extra_hours * self.extra_hour_price)

class GuideAvailability(models.Model):
    """
    Guide availability calendar for advanced time slot management
    """
    TIME_SLOTS = [
        ('morning', 'Morning (8:00-12:00)'),
        ('afternoon', 'Afternoon (13:00-17:00)'),
        ('evening', 'Evening (18:00-22:00)'),
        ('full_day', 'Full Day (8:00-17:00)'),
    ]
    
    guide = models.ForeignKey(
        GuideProfile,
        on_delete=models.CASCADE,
        related_name='availability_slots'
    )
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'guide_availability'
        unique_together = ['guide', 'date', 'time_slot']
        indexes = [
            models.Index(fields=['guide', 'date']),
            models.Index(fields=['date', 'is_available']),
        ]
    
    def __str__(self):
        return f"{self.guide.user.username} - {self.date} ({self.time_slot})"

class GuideCertification(models.Model):
    """
    Guide certifications and documents
    """
    guide = models.ForeignKey(
        GuideProfile, 
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='guides/certifications/')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'guide_certifications'
    
    def __str__(self):
        return f"{self.guide.user.username} - {self.title}"
