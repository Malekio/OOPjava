from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Review

# Placeholder views - will be implemented properly
class TourReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.AllowAny]

class GuideReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.AllowAny]

class BookingReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.AllowAny]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.AllowAny]
