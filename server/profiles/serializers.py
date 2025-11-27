from rest_framework import serializers
from .models import TouristProfile, GuideProfile, GuideCertification
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
