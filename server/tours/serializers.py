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
            "id",
            "title",
            "description",
            "guide",
            "wilaya",
            "duration_hours",
            "price",
            "max_group_size",
            "primary_image",
            "created_at",
            "slug",
        ]

    def get_primary_image(self, obj):
        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None


class TourDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for tour information
    """

    guide = GuideProfileListSerializer(read_only=True)
    wilaya = WilayaSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    weather_forecast = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "title",
            "description",
            "guide",
            "wilaya",
            "duration_hours",
            "price",
            "max_group_size",
            "included_services",
            "excluded_services",
            "meeting_point",
            "latitude",
            "longitude",
            "image_url",
            "tags",
            "weather_forecast",
            "created_at",
            "updated_at",
            "slug",
        ]

    def get_image_url(self, obj):
        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None

    def get_weather_forecast(self, obj):
        """
        Get weather forecast if date is provided in context
        """
        request = self.context.get("request")
        if request and hasattr(request, "query_params"):
            booking_date = request.query_params.get("date")
            if booking_date and obj.latitude and obj.longitude:
                from server.utils.weather_service import WeatherService

                return WeatherService.get_weather_forecast(
                    float(obj.latitude), float(obj.longitude), booking_date
                )
        return None


class TourCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating tours
    """

    class Meta:
        model = Tour
        fields = [
            "title",
            "description",
            "wilaya",
            "duration_hours",
            "max_group_size",
            "included_services",
            "excluded_services",
            "meeting_point",
            "latitude",
            "longitude",
            "tags",
            "image",
        ]

    def validate(self, data):
        """
        Validate GPS coordinates are provided for new tours or when being updated
        """
        # For updates (PATCH), only validate if latitude or longitude is being changed
        if self.instance:  # This is an update
            # Only validate if either coordinate is being updated
            if "latitude" in data or "longitude" in data:
                # If one is provided, both must be provided
                latitude = data.get("latitude", self.instance.latitude)
                longitude = data.get("longitude", self.instance.longitude)
                if not latitude or not longitude:
                    raise serializers.ValidationError(
                        "Both latitude and longitude are required for weather integration."
                    )
        else:  # This is a create operation
            if not data.get("latitude") or not data.get("longitude"):
                raise serializers.ValidationError(
                    "GPS coordinates (latitude and longitude) are required for weather integration."
                )
        return data


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
