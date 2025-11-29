from rest_framework import serializers
from .models import Conversation, Message, CustomTourRequest

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages
    """
    class Meta:
        model = Message
        fields = ['id', 'sender_type', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversations with recent messages
    """
    tourist_name = serializers.CharField(source='tourist.user.username', read_only=True)
    guide_name = serializers.CharField(source='guide.user.username', read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'tourist_name', 'guide_name', 'subject', 
            'last_message', 'unread_count', 'last_message_at', 'created_at'
        ]
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        return MessageSerializer(last_msg).data if last_msg else None
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        user_type = 'tourist' if hasattr(user, 'tourist_profile') else 'guide'
        # Count messages not sent by current user and not read
        return obj.messages.exclude(sender_type=user_type).filter(is_read=False).count()

class CustomTourRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for custom tour requests
    """
    tourist_name = serializers.CharField(source='tourist.user.username', read_only=True)
    guide_name = serializers.CharField(source='guide.user.username', read_only=True)
    
    class Meta:
        model = CustomTourRequest
        fields = [
            'id', 'tourist_name', 'guide_name', 'title', 'description',
            'preferred_date', 'duration_hours', 'group_size', 'budget',
            'special_requirements', 'status', 'guide_response', 
            'proposed_price', 'alternative_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'tourist_name', 'guide_name', 'created_at', 'updated_at']

class CustomTourRequestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating custom tour requests
    """
    class Meta:
        model = CustomTourRequest
        fields = [
            'guide', 'title', 'description', 'preferred_date', 
            'duration_hours', 'group_size', 'budget', 'special_requirements'
        ]
