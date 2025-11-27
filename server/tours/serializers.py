from rest_framework import serializers
from .models import Tour
from profiles.serializers import GuideProfileListSerializer
from locations.serializers import WilayaSerializer

class TourListSerializer(serializers.ModelSerializer):
    """
    Serializer for tour listings
    """
    guide = GuideProfileListSerializer(read_only=True)
    wilaya = WilayaSerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'guide', 'wilaya',
            'duration_hours', 'price', 'max_group_size',
            'primary_image', 'created_at', 'slug'
        ]
    
    def get_primary_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class TourDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for tour information
    """
    guide = GuideProfileListSerializer(read_only=True)
    wilaya = WilayaSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'guide', 'wilaya',
            'duration_hours', 'price', 'max_group_size',
            'included_services', 'excluded_services', 'meeting_point',
            'image_url', 'tags', 'created_at', 'updated_at', 'slug'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class TourCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating tours
    """
    class Meta:
        model = Tour
        fields = [
            'title', 'description', 'wilaya', 'duration_hours',
            'max_group_size', 'included_services', 'excluded_services',
            'meeting_point', 'tags', 'image'
        ]

class TourPriceCalculationSerializer(serializers.Serializer):
    """
    Serializer for calculating tour price based on custom duration
    """
    duration_hours = serializers.DecimalField(max_digits=4, decimal_places=1)
    
    def validate_duration_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than 0")
        if value > 24:
            raise serializers.ValidationError("Duration cannot exceed 24 hours")
        return value
