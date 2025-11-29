from rest_framework import serializers
from django.utils import timezone
from .models import Booking
from tours.serializers import TourListSerializer
from profiles.serializers import TouristProfileSerializer, GuideProfileListSerializer

class BookingSerializer(serializers.ModelSerializer):
    """
    Complete booking serializer with relationships
    """
    tour = TourListSerializer(read_only=True)
    tourist = TouristProfileSerializer(read_only=True)
    tour_id = serializers.IntegerField(write_only=True)
    days_until_booking = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()
    can_review = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'tour', 'tourist', 'tour_id',
            'booking_date', 'time_slot', 'group_size', 'total_price',
            'status', 'notes', 'days_until_booking', 'can_cancel',
            'can_review', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at', 'updated_at']
    
    def get_days_until_booking(self, obj):
        """Calculate days until booking date"""
        today = timezone.now().date()
        return (obj.booking_date - today).days
    
    def get_can_cancel(self, obj):
        """Check if booking can be cancelled (24+ hours before)"""
        if obj.status in ['completed', 'cancelled']:
            return False
        return self.get_days_until_booking(obj) >= 1
    
    def get_can_review(self, obj):
        """Check if booking can be reviewed (completed only)"""
        return obj.status == 'completed'
    
    def validate_booking_date(self, value):
        """Ensure booking date is in the future"""
        if value <= timezone.now().date():
            raise serializers.ValidationError(
                "Booking date must be in the future."
            )
        return value
    
    def validate_group_size(self, value):
        """Validate group size against tour limits"""
        if value <= 0:
            raise serializers.ValidationError(
                "Group size must be greater than 0."
            )
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        tour_id = data.get('tour_id')
        group_size = data.get('group_size', 1)
        
        if tour_id:
            from tours.models import Tour
            try:
                tour = Tour.objects.get(id=tour_id)
                if group_size > tour.max_group_size:
                    raise serializers.ValidationError({
                        'group_size': f'Group size cannot exceed {tour.max_group_size} for this tour.'
                    })
                data['total_price'] = tour.price * group_size
            except Tour.DoesNotExist:
                raise serializers.ValidationError({
                    'tour_id': 'Invalid tour ID.'
                })
        
        return data

class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings
    """
    class Meta:
        model = Booking
        fields = [
            'tour', 'booking_date', 'time_slot', 'group_size', 'notes'
        ]
    
    def validate_booking_date(self, value):
        """Ensure booking date is in the future"""
        if value <= timezone.now().date():
            raise serializers.ValidationError(
                "Booking date must be in the future."
            )
        return value

class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating booking status
    """
    action = serializers.ChoiceField(
        choices=['confirm', 'reject', 'complete'],
        write_only=True
    )
    alternative_date = serializers.DateField(required=False, allow_null=True)
    alternative_time_slot = serializers.ChoiceField(
        choices=Booking._meta.get_field('time_slot').choices,
        required=False,
        allow_null=True
    )
    rejection_reason = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'action', 'alternative_date', 'alternative_time_slot', 
            'rejection_reason', 'notes'
        ]
    
    def validate_alternative_date(self, value):
        """Validate alternative date if provided"""
        if value and value <= timezone.now().date():
            raise serializers.ValidationError(
                "Alternative date must be in the future."
            )
        return value

class BookingListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing bookings
    """
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    tourist_name = serializers.CharField(source='tourist.user.get_full_name', read_only=True)
    guide_name = serializers.CharField(source='tour.guide.user.get_full_name', read_only=True)
    days_until_booking = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'tour_title', 'tourist_name', 'guide_name',
            'booking_date', 'time_slot', 'group_size', 'total_price',
            'status', 'days_until_booking', 'created_at'
        ]
    
    def get_days_until_booking(self, obj):
        """Calculate days until booking date"""
        today = timezone.now().date()
        return (obj.booking_date - today).days
