from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Booking
from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
    BookingListSerializer,
    BookingStatusUpdateSerializer,
)
from tours.models import Tour
from profiles.models import GuideAvailability


class BookingListCreateView(generics.ListCreateAPIView):
    """
    List user's bookings and create new booking requests
    """

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "booking_date", "time_slot"]
    ordering_fields = ["booking_date", "created_at"]
    ordering = ["-booking_date"]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "tourist_profile"):
            return Booking.objects.filter(tourist=user.tourist_profile).select_related(
                "tour", "tour__guide", "tourist"
            )
        return Booking.objects.none()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer
        return BookingListSerializer

    def perform_create(self, serializer):
        """Create booking with calculated total price"""
        if not hasattr(self.request.user, "tourist_profile"):
            raise permissions.PermissionDenied("Only tourists can create bookings.")

        tour = serializer.validated_data["tour"]
        group_size = serializer.validated_data["group_size"]
        total_price = tour.price * group_size

        serializer.save(
            tourist=self.request.user.tourist_profile, total_price=total_price
        )


class BookingDetailView(generics.RetrieveAPIView):
    """
    Get booking details with permission checks
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.select_related("tour", "tour__guide", "tourist")

        # Filter based on user type
        if hasattr(user, "tourist_profile"):
            return queryset.filter(tourist=user.tourist_profile)
        elif hasattr(user, "guide_profile"):
            return queryset.filter(tour__guide=user.guide_profile)
        return queryset.none()


class BookingStatusUpdateView(generics.UpdateAPIView):
    """
    Guide updates booking status (confirm/reject/complete)
    """

    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "guide_profile"):
            return Booking.objects.filter(tour__guide=user.guide_profile)
        return Booking.objects.none()

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            action = serializer.validated_data["action"]

            # Validate status transitions
            if booking.status == "completed":
                return Response(
                    {"error": "Cannot modify completed booking"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if booking.status == "cancelled":
                return Response(
                    {"error": "Cannot modify cancelled booking"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Handle different actions
            if action == "confirm":
                if booking.status != "pending":
                    return Response(
                        {"error": "Only pending bookings can be confirmed"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                booking.status = "confirmed"

            elif action == "reject":
                if booking.status != "pending":
                    return Response(
                        {"error": "Only pending bookings can be rejected"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                booking.status = "cancelled"

                # Handle alternative date/time proposal
                alt_date = serializer.validated_data.get("alternative_date")
                alt_time = serializer.validated_data.get("alternative_time_slot")
                rejection_reason = serializer.validated_data.get("rejection_reason", "")

                if alt_date or alt_time:
                    notes = f"Alternative proposal: "
                    if alt_date:
                        notes += f"Date: {alt_date} "
                    if alt_time:
                        notes += f"Time: {alt_time} "
                    if rejection_reason:
                        notes += f"Reason: {rejection_reason}"
                    booking.notes = notes
                elif rejection_reason:
                    booking.notes = f"Rejection reason: {rejection_reason}"

            elif action == "complete":
                if booking.status != "confirmed":
                    return Response(
                        {"error": "Only confirmed bookings can be completed"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Check if booking date has passed
                if booking.booking_date > timezone.now().date():
                    return Response(
                        {"error": "Cannot complete future bookings"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                booking.status = "completed"

                # Update guide's total completed tours
                guide = booking.tour.guide
                guide.total_tours_completed += 1
                guide.save()

            # Update notes if provided
            if "notes" in serializer.validated_data:
                booking.notes = serializer.validated_data["notes"]

            booking.save()

            return Response(
                BookingSerializer(booking, context={"request": request}).data
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCancelView(generics.UpdateAPIView):
    """
    Cancel booking (tourist or guide can cancel)
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.select_related("tour", "tour__guide", "tourist")

        if hasattr(user, "tourist_profile"):
            return queryset.filter(tourist=user.tourist_profile)
        elif hasattr(user, "guide_profile"):
            return queryset.filter(tour__guide=user.guide_profile)
        return queryset.none()

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        # Validate cancellation
        if booking.status in ["completed", "cancelled"]:
            return Response(
                {"error": f"Cannot cancel {booking.status} booking"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check 24-hour cancellation policy
        days_until_booking = (booking.booking_date - timezone.now().date()).days
        if days_until_booking < 1:
            return Response(
                {"error": "Cannot cancel bookings less than 24 hours before tour date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = "cancelled"
        booking.save()

        return Response(BookingSerializer(booking, context={"request": request}).data)


class BookingInvoiceView(generics.RetrieveAPIView):
    """
    Get booking invoice/receipt details
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.select_related(
            "tour", "tour__guide", "tourist"
        ).filter(status__in=["confirmed", "completed"])

        if hasattr(user, "tourist_profile"):
            return queryset.filter(tourist=user.tourist_profile)
        elif hasattr(user, "guide_profile"):
            return queryset.filter(tour__guide=user.guide_profile)
        return queryset.none()


class GuidePendingBookingsView(generics.ListAPIView):
    """
    Guide's dashboard - pending bookings requiring action
    """

    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "guide_profile"):
            return Booking.objects.filter(
                tour__guide=user.guide_profile, status="pending"
            ).select_related("tour", "tourist")
        return Booking.objects.none()


class TouristUpcomingBookingsView(generics.ListAPIView):
    """
    Tourist's upcoming confirmed bookings
    """

    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["booking_date"]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "tourist_profile"):
            today = timezone.now().date()
            return Booking.objects.filter(
                tourist=user.tourist_profile,
                status="confirmed",
                booking_date__gte=today,
            ).select_related("tour", "tour__guide")
        return Booking.objects.none()


class GuideAvailabilityCalendarView(generics.ListAPIView):
    """
    Guide's availability calendar
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, "guide_profile"):
            return Response(
                {"error": "Only guides can access availability calendar"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get date range (default: next 30 days)
        from datetime import datetime, timedelta

        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)

        # Get availability slots
        availability_slots = GuideAvailability.objects.filter(
            guide=user.guide_profile, date__range=[start_date, end_date]
        ).order_by("date", "time_slot")

        # Get existing bookings
        bookings = Booking.objects.filter(
            tour__guide=user.guide_profile,
            booking_date__range=[start_date, end_date],
            status__in=["confirmed", "pending"],
        ).values("booking_date", "time_slot", "status")

        # Combine data
        calendar_data = []
        for slot in availability_slots:
            # Check if there's a booking for this slot
            booking_info = next(
                (
                    b
                    for b in bookings
                    if b["booking_date"] == slot.date
                    and b["time_slot"] == slot.time_slot
                ),
                None,
            )

            calendar_data.append(
                {
                    "date": slot.date,
                    "time_slot": slot.time_slot,
                    "is_available": slot.is_available,
                    "booking_status": booking_info["status"] if booking_info else None,
                }
            )

        return Response(calendar_data)
