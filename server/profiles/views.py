from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TouristProfile, GuideProfile, GuideCertification, GuideAvailability
from .serializers import (
    TouristProfileSerializer,
    GuideProfileSerializer,
    GuideProfileListSerializer,
    GuideProfileUpdateSerializer,
    GuideCertificationSerializer,
    GuidePricingSerializer,
    GuideAvailabilitySerializer,
    GuideAvailabilityBulkSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsGuideOwner
from .filters import GuideProfileFilter


class GuideProfileListView(generics.ListAPIView):
    """
    List all verified guides with filtering and search
    """

    queryset = GuideProfile.objects.filter(
        verification_status="verified"
    ).select_related("user")
    serializer_class = GuideProfileListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GuideProfileFilter
    search_fields = ["user__first_name", "user__last_name", "bio", "languages"]
    ordering_fields = ["average_rating", "total_reviews", "created_at"]
    ordering = ["-average_rating"]


class GuideProfileDetailView(generics.RetrieveAPIView):
    """
    Get specific guide details
    """

    serializer_class = GuideProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user_id = self.kwargs["pk"]  # This is the User ID from URL
        return GuideProfile.objects.get(
            user__id=user_id, verification_status="verified"
        )


class GuideProfileMeView(generics.RetrieveUpdateAPIView):
    """
    Get and update current guide's profile
    """

    serializer_class = GuideProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsGuideOwner]

    def get_object(self):
        return self.request.user.guide_profile

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return GuideProfileUpdateSerializer
        return GuideProfileSerializer


class TouristProfileMeView(generics.RetrieveUpdateAPIView):
    """
    Get and update current tourist's profile
    """

    serializer_class = TouristProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = TouristProfile.objects.get_or_create(user=self.request.user)
        return profile


class GuideCertificationListCreateView(generics.ListCreateAPIView):
    """
    List and create guide certifications
    """

    serializer_class = GuideCertificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsGuideOwner]

    def get_queryset(self):
        return GuideCertification.objects.filter(guide=self.request.user.guide_profile)

    def perform_create(self, serializer):
        serializer.save(guide=self.request.user.guide_profile)


class GuideCertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete guide certifications
    """

    serializer_class = GuideCertificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsGuideOwner]

    def get_queryset(self):
        return GuideCertification.objects.filter(guide=self.request.user.guide_profile)


class GuidePricingView(generics.RetrieveAPIView):
    """
    Get guide's pricing structure
    """

    serializer_class = GuidePricingSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user_id = self.kwargs["pk"]  # This is the User ID from URL
        return GuideProfile.objects.get(
            user__id=user_id, verification_status="verified"
        )


class GuideAvailabilityManagementView(APIView):
    """
    Manage guide availability - CRUD operations for availability slots
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get guide's availability (next 60 days)
        """
        if not hasattr(request.user, "guide_profile"):
            return Response(
                {"error": "Only guides can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN,
            )

        from datetime import timedelta
        from django.utils import timezone

        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=60)

        availability = GuideAvailability.objects.filter(
            guide=request.user.guide_profile, date__range=[start_date, end_date]
        ).order_by("date", "time_slot")

        serializer = GuideAvailabilitySerializer(availability, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
                "total_slots": availability.count(),
            }
        )

    def post(self, request):
        """
        Create new availability slot

        Request format:
        {
            "date": "2025-12-15",
            "time_slot": "morning",  // morning|afternoon|evening|full_day
            "is_available": true
        }
        """
        if not hasattr(request.user, "guide_profile"):
            return Response(
                {"error": "Only guides can manage availability"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = GuideAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            # Check if slot already exists
            existing = GuideAvailability.objects.filter(
                guide=request.user.guide_profile,
                date=serializer.validated_data["date"],
                time_slot=serializer.validated_data["time_slot"],
            ).first()

            if existing:
                return Response(
                    {
                        "error": "Availability slot already exists for this date and time",
                        "existing_slot": GuideAvailabilitySerializer(existing).data,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new slot
            availability = serializer.save(guide=request.user.guide_profile)
            return Response(
                {
                    "success": True,
                    "message": "Availability slot created successfully",
                    "data": GuideAvailabilitySerializer(availability).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request):
        """
        Update existing availability slot

        Request format:
        {
            "id": 123,
            "date": "2025-12-15",
            "time_slot": "morning",
            "is_available": false
        }
        """
        if not hasattr(request.user, "guide_profile"):
            return Response(
                {"error": "Only guides can manage availability"},
                status=status.HTTP_403_FORBIDDEN,
            )

        slot_id = request.data.get("id")
        if not slot_id:
            return Response(
                {"error": "Slot ID is required for updates"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            availability = GuideAvailability.objects.get(
                id=slot_id, guide=request.user.guide_profile
            )
        except GuideAvailability.DoesNotExist:
            return Response(
                {"error": "Availability slot not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = GuideAvailabilitySerializer(
            availability, data=request.data, partial=True
        )
        if serializer.is_valid():
            availability = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Availability updated successfully",
                    "data": GuideAvailabilitySerializer(availability).data,
                }
            )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        """
        Delete availability slot

        Request format:
        {
            "id": 123
        }
        """
        if not hasattr(request.user, "guide_profile"):
            return Response(
                {"error": "Only guides can manage availability"},
                status=status.HTTP_403_FORBIDDEN,
            )

        slot_id = request.data.get("id")
        if not slot_id:
            return Response(
                {"error": "Slot ID is required for deletion"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            availability = GuideAvailability.objects.get(
                id=slot_id, guide=request.user.guide_profile
            )
            availability.delete()
            return Response(
                {"success": True, "message": "Availability slot deleted successfully"}
            )
        except GuideAvailability.DoesNotExist:
            return Response(
                {"error": "Availability slot not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class GuideAvailabilityBulkView(APIView):
    """
    Bulk operations for guide availability
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Create multiple availability slots

        Request format:
        {
            "start_date": "2025-12-01",
            "end_date": "2025-12-07",
            "time_slots": ["morning", "afternoon"],
            "is_available": true
        }
        """
        if not hasattr(request.user, "guide_profile"):
            return Response(
                {"error": "Only guides can manage availability"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = GuideAvailabilityBulkSerializer(data=request.data)
        if serializer.is_valid():
            from datetime import timedelta

            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            time_slots = serializer.validated_data["time_slots"]
            is_available = serializer.validated_data["is_available"]

            created_slots = []
            skipped_slots = []

            current_date = start_date
            while current_date <= end_date:
                for time_slot in time_slots:
                    # Check if slot already exists
                    existing = GuideAvailability.objects.filter(
                        guide=request.user.guide_profile,
                        date=current_date,
                        time_slot=time_slot,
                    ).first()

                    if existing:
                        skipped_slots.append(
                            {
                                "date": current_date,
                                "time_slot": time_slot,
                                "reason": "Already exists",
                            }
                        )
                    else:
                        # Create new slot
                        new_slot = GuideAvailability.objects.create(
                            guide=request.user.guide_profile,
                            date=current_date,
                            time_slot=time_slot,
                            is_available=is_available,
                        )
                        created_slots.append(GuideAvailabilitySerializer(new_slot).data)

                current_date += timedelta(days=1)

            return Response(
                {
                    "success": True,
                    "message": f"Bulk operation completed",
                    "summary": {
                        "created": len(created_slots),
                        "skipped": len(skipped_slots),
                    },
                    "created_slots": created_slots,
                    "skipped_slots": skipped_slots,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
