from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Review
from .serializers import (
    ReviewSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    ReviewListSerializer,
    GuideResponseSerializer,
)
from bookings.models import Booking
from profiles.models import GuideProfile
from tours.models import Tour


class TourReviewListView(generics.ListAPIView):
    """
    List all reviews for a specific tour
    """

    serializer_class = ReviewListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["rating", "is_approved"]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        tour_id = self.kwargs.get("tour_id")
        return Review.objects.filter(tour_id=tour_id, is_approved=True).select_related(
            "tourist", "guide", "tour"
        )


class GuideReviewListView(generics.ListAPIView):
    """
    List all reviews for a specific guide
    """

    serializer_class = ReviewListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["rating", "is_approved"]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        guide_id = self.kwargs.get("guide_id")
        return Review.objects.filter(
            guide_id=guide_id, is_approved=True
        ).select_related("tourist", "guide", "tour")


class BookingReviewCreateView(generics.CreateAPIView):
    """
    Create review for a completed booking
    """

    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def create(self, request, *args, **kwargs):
        # Get booking from URL parameter
        booking_id = self.kwargs.get("booking_id")

        # Validate user is a tourist
        if not hasattr(request.user, "tourist_profile"):
            return Response(
                {"error": "Only tourists can create reviews"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get and validate booking
        booking = get_object_or_404(
            Booking.objects.select_related("tour", "tour__guide", "tourist"),
            id=booking_id,
        )

        # Check if user owns this booking
        if booking.tourist != request.user.tourist_profile:
            return Response(
                {"error": "You can only review your own bookings"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if booking is completed
        if booking.status != "completed":
            return Response(
                {"error": "You can only review completed bookings"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if review already exists
        if hasattr(booking, "review"):
            return Response(
                {"error": "A review already exists for this booking"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create review with booking relationships
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            review = Review.objects.create(
                booking=booking,
                tourist=booking.tourist,
                guide=booking.tour.guide,
                tour=booking.tour,
                rating=serializer.validated_data["rating"],
                title=serializer.validated_data["title"],
                comment=serializer.validated_data["comment"],
            )

            return Response(
                ReviewSerializer(review, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete review (tourists can edit their own reviews)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.select_related("tourist", "guide", "tour", "booking")

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        """
        Different permissions for different actions
        """
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        review = self.get_object()

        # Check if user owns this review
        if (
            not hasattr(request.user, "tourist_profile")
            or review.tourist != request.user.tourist_profile
        ):
            return Response(
                {"error": "You can only edit your own reviews"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()

        # Check if user owns this review
        if (
            not hasattr(request.user, "tourist_profile")
            or review.tourist != request.user.tourist_profile
        ):
            return Response(
                {"error": "You can only delete your own reviews"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def guide_respond_to_review(request, review_id):
    """
    Allow guides to respond to reviews about them
    """
    if not hasattr(request.user, "guide_profile"):
        return Response(
            {"error": "Only guides can respond to reviews"},
            status=status.HTTP_403_FORBIDDEN,
        )

    review = get_object_or_404(Review.objects.select_related("guide"), id=review_id)

    # Check if guide owns this review
    if review.guide != request.user.guide_profile:
        return Response(
            {"error": "You can only respond to reviews about you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if guide already responded
    if review.guide_response:
        return Response(
            {"error": "You have already responded to this review"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = GuideResponseSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        review.guide_response = serializer.validated_data["guide_response"]
        review.guide_responded_at = timezone.now()
        review.save()

        return Response(ReviewSerializer(review, context={"request": request}).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def review_statistics(request, guide_id):
    """
    Get review statistics for a guide
    """
    guide = get_object_or_404(GuideProfile, pk=guide_id)

    reviews = Review.objects.filter(guide=guide, is_approved=True)

    if not reviews.exists():
        return Response(
            {
                "total_reviews": 0,
                "average_rating": 0,
                "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            }
        )

    # Calculate statistics
    total_reviews = reviews.count()
    average_rating = sum(r.rating for r in reviews) / total_reviews

    # Rating distribution
    rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        rating_distribution[review.rating] += 1

    return Response(
        {
            "total_reviews": total_reviews,
            "average_rating": round(average_rating, 2),
            "rating_distribution": rating_distribution,
        }
    )
