from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from profiles.models import GuideProfile
from locations.models import Wilaya
from decimal import Decimal

class Tour(models.Model):
    """
    Tour packages created by guides
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    guide = models.ForeignKey(
        GuideProfile,
        on_delete=models.CASCADE,
        related_name='tours'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    duration_hours = models.DecimalField(
        max_digits=4, 
        decimal_places=1,
        help_text="Duration in hours"
    )
    max_group_size = models.PositiveIntegerField(default=8)
    included_services = models.JSONField(default=list)  # List of included services
    excluded_services = models.JSONField(default=list)  # List of excluded services
    meeting_point = models.CharField(max_length=200)
    
    # Calculated price based on guide's pricing structure
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # SEO and discoverability
    slug = models.SlugField(unique=True, blank=True)
    tags = models.JSONField(default=list)  # Search tags
    
    # Tour image
    image = models.ImageField(upload_to='tours/images/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tours'
        indexes = [
            models.Index(fields=['wilaya']),
            models.Index(fields=['status']),
            models.Index(fields=['price']),
            models.Index(fields=['duration_hours']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.guide.user.username}"
    
    def clean(self):
        """
        Validate that tour location is within guide's coverage areas
        """
        if self.wilaya and self.guide:
            if not self.guide.coverage_areas.filter(id=self.wilaya.id).exists():
                raise ValidationError({
                    'wilaya': 'Tour location must be within your coverage areas.'
                })
    
    def save(self, *args, **kwargs):
        # Auto-calculate price based on duration and guide's pricing
        if self.guide and self.duration_hours:
            self.price = self.guide.calculate_tour_price(float(self.duration_hours))
        
        # Generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = f"{slugify(self.title)}-{str(uuid.uuid4())[:8]}"
        
        self.clean()
        super().save(*args, **kwargs)
