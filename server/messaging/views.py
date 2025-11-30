from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, CustomTourRequest
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    CustomTourRequestSerializer,
    CustomTourRequestCreateSerializer,
)
from profiles.models import TouristProfile, GuideProfile


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """

    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "tourist_profile"):
            return Conversation.objects.filter(tourist=user.tourist_profile)
        elif hasattr(user, "guide_profile"):
            return Conversation.objects.filter(guide=user.guide_profile)
        return Conversation.objects.none()

    def create(self, request):
        """
        Create or get existing conversation
        """
        guide_id = request.data.get("guide_id")
        if not hasattr(request.user, "tourist_profile"):
            return Response(
                {"error": "Only tourists can start conversations"},
                status=status.HTTP_403_FORBIDDEN,
            )

        guide = get_object_or_404(GuideProfile, pk=guide_id)
        conversation, created = Conversation.objects.get_or_create(
            tourist=request.user.tourist_profile, guide=guide
        )

        return Response(
            ConversationSerializer(conversation, context={"request": request}).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """
        Get all messages in a conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Send a message in a conversation
        """
        conversation = self.get_object()
        user = request.user

        # Determine sender type
        if (
            hasattr(user, "tourist_profile")
            and conversation.tourist == user.tourist_profile
        ):
            sender_type = "tourist"
        elif (
            hasattr(user, "guide_profile") and conversation.guide == user.guide_profile
        ):
            sender_type = "guide"
        else:
            return Response(
                {"error": "Not authorized for this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender_type=sender_type,
            content=request.data.get("content", ""),
        )

        # Update conversation timestamp
        conversation.last_message_at = message.created_at
        conversation.save()

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        """
        Mark messages as read
        """
        conversation = self.get_object()
        user = request.user

        # Determine user type to mark messages from other party as read
        if hasattr(user, "tourist_profile"):
            conversation.messages.filter(sender_type="guide", is_read=False).update(
                is_read=True
            )
        elif hasattr(user, "guide_profile"):
            conversation.messages.filter(sender_type="tourist", is_read=False).update(
                is_read=True
            )

        return Response({"status": "Messages marked as read"})


class CustomTourRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing custom tour requests
    """

    serializer_class = CustomTourRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "tourist_profile"):
            return CustomTourRequest.objects.filter(tourist=user.tourist_profile)
        elif hasattr(user, "guide_profile"):
            return CustomTourRequest.objects.filter(guide=user.guide_profile)
        return CustomTourRequest.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return CustomTourRequestCreateSerializer
        return CustomTourRequestSerializer

    def create(self, request):
        """
        Create a custom tour request
        """
        if not hasattr(request.user, "tourist_profile"):
            return Response(
                {"error": "Only tourists can create custom tour requests"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tourist=request.user.tourist_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def respond(self, request, pk=None):
        """
        Guide responds to custom tour request
        """
        custom_request = self.get_object()

        if (
            not hasattr(request.user, "guide_profile")
            or custom_request.guide != request.user.guide_profile
        ):
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )

        action_type = request.data.get("action")  # 'accept' or 'reject'

        if action_type == "accept":
            custom_request.status = "accepted"
            custom_request.proposed_price = request.data.get("proposed_price")
            custom_request.alternative_date = request.data.get("alternative_date")
        elif action_type == "reject":
            custom_request.status = "rejected"

        custom_request.guide_response = request.data.get("guide_response", "")
        custom_request.save()

        return Response(CustomTourRequestSerializer(custom_request).data)
