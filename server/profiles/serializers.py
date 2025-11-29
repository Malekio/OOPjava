from rest_framework import serializers
from .models import TouristProfile, GuideProfile, GuideCertification, GuideAvailability
from locations.models import Wilaya
from accounts.serializers import UserSerializer

class WilayaSerializer(serializers.ModelSerializer):
    """
    Serializer for Wilaya model
    """
    class Meta:
        model = Wilaya
        fields = ['id', 'code', 'name_ar', 'name_en', 'name_fr']

class TouristProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Tourist Profile
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TouristProfile
        fields = [
            'user', 'bio', 'date_of_birth', 'nationality', 
            'preferred_language', 'profile_picture', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']

class GuideCertificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Guide Certifications
    """
    class Meta:
        model = GuideCertification
        fields = [
            'id', 'title', 'document', 'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at']

class GuideProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Guide Profile
    """
    user = UserSerializer(read_only=True)
    coverage_areas = WilayaSerializer(many=True, read_only=True)
    coverage_area_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Wilaya.objects.all(),
        source='coverage_areas',
        write_only=True
    )
    certifications = GuideCertificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = GuideProfile
        fields = [
            'user', 'bio', 'profile_picture', 'years_of_experience',
            'languages', 'coverage_areas', 'coverage_area_ids',
            'half_day_price', 'full_day_price', 'extra_hour_price',
            'verification_status', 'average_rating', 'total_reviews',
            'total_tours_completed', 'certifications', 'created_at'
        ]
        read_only_fields = [
            'user', 'verification_status', 'average_rating', 
            'total_reviews', 'total_tours_completed', 'created_at'
        ]

class GuideProfileListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for guide listings
    """
    user = UserSerializer(read_only=True)
    coverage_areas = WilayaSerializer(many=True, read_only=True)
    
    class Meta:
        model = GuideProfile
        fields = [
            'user', 'bio', 'profile_picture', 'years_of_experience',
            'languages', 'coverage_areas', 'half_day_price', 
            'full_day_price', 'verification_status', 'average_rating',
            'total_reviews', 'total_tours_completed'
        ]

class GuideProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating guide profile
    """
    coverage_area_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Wilaya.objects.all(),
        source='coverage_areas'
    )
    
    class Meta:
        model = GuideProfile
        fields = [
            'bio', 'profile_picture', 'years_of_experience', 'languages',
            'coverage_area_ids', 'half_day_price', 'full_day_price', 'extra_hour_price'
        ]

class GuidePricingSerializer(serializers.ModelSerializer):
    """
    Serializer for guide pricing information
    """
    class Meta:
        model = GuideProfile
        fields = ['half_day_price', 'full_day_price', 'extra_hour_price']

class GuideAvailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for Guide Availability management
    """
    class Meta:
        model = GuideAvailability
        fields = ['id', 'date', 'time_slot', 'is_available', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_date(self, value):
        """
        Ensure guides can't set availability for past dates
        """
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Cannot set availability for past dates")
        return value

class GuideAvailabilityBulkSerializer(serializers.Serializer):
    """
    Serializer for bulk availability operations
    """
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    time_slots = serializers.MultipleChoiceField(
        choices=GuideAvailability.TIME_SLOTS,
        allow_empty=False
    )
    is_available = serializers.BooleanField(default=True)
    
    def validate(self, data):
        """
        Validate date range
        """
        from django.utils import timezone
        from datetime import timedelta
        
        start_date = data['start_date']
        end_date = data['end_date']
        
        # Check if dates are not in the past
        if start_date < timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the past")
        
        # Check if end date is after start date
        if end_date < start_date:
            raise serializers.ValidationError("End date must be after start date")
        
        # Limit range to prevent abuse (max 90 days)
        if (end_date - start_date).days > 90:
            raise serializers.ValidationError("Date range cannot exceed 90 days")
        
        return data
