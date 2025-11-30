from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review
from bookings.models import Booking
from profiles.serializers import TouristProfileSerializer, GuideProfileListSerializer
from tours.serializers import TourListSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """
    Complete review serializer with relationships
    """

    tourist = TouristProfileSerializer(read_only=True)
    guide = GuideProfileListSerializer(read_only=True)
    tour = TourListSerializer(read_only=True)
    tourist_name = serializers.CharField(
        source="tourist.user.get_full_name", read_only=True
    )
    guide_name = serializers.CharField(
        source="guide.user.get_full_name", read_only=True
    )
    tour_title = serializers.CharField(source="tour.title", read_only=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "tourist",
            "guide",
            "tour",
            "booking",
            "tourist_name",
            "guide_name",
            "tour_title",
            "rating",
            "title",
            "comment",
            "can_edit",
            "is_approved",
            "is_featured",
            "guide_response",
            "guide_responded_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "tourist",
            "guide",
            "tour",
            "booking",
            "is_approved",
            "is_featured",
            "guide_response",
            "guide_responded_at",
            "created_at",
            "updated_at",
        ]

    def get_can_edit(self, obj):
        """Check if current user can edit this review"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return (
                hasattr(request.user, "tourist_profile")
                and obj.tourist == request.user.tourist_profile
            )
        return False

    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating reviews
    booking_id comes from URL parameter, not request body
    """

    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]

    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value

    def create(self, validated_data):
        """Create review with proper relationships"""
        booking_id = validated_data.pop("booking_id")
        booking = Booking.objects.get(id=booking_id)

        review = Review.objects.create(
            booking=booking,
            tourist=booking.tourist,
            guide=booking.tour.guide,
            tour=booking.tour,
            **validated_data,
        )
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating reviews (tourists can only update their own)
    """

    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]

    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value


class GuideResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for guide responses to reviews
    """

    class Meta:
        model = Review
        fields = ["guide_response"]

    def validate_guide_response(self, value):
        """Validate guide response is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Guide response cannot be empty.")
        return value.strip()


class ReviewListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing reviews
    """

    tourist_name = serializers.CharField(
        source="tourist.user.get_full_name", read_only=True
    )
    guide_name = serializers.CharField(
        source="guide.user.get_full_name", read_only=True
    )
    tour_title = serializers.CharField(source="tour.title", read_only=True)
    tourist_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "tourist_name",
            "guide_name",
            "tour_title",
            "tourist_avatar",
            "rating",
            "title",
            "comment",
            "guide_response",
            "created_at",
        ]

    def get_tourist_avatar(self, obj):
        """Get tourist profile picture URL"""
        if obj.tourist.profile_picture:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.tourist.profile_picture.url)
        return None
