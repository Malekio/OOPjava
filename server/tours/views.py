from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Tour
from .serializers import (
    TourListSerializer,
    TourDetailSerializer,
    TourCreateUpdateSerializer,
    TourPriceCalculationSerializer
)

# Placeholder views - will be implemented properly
class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourListSerializer
    permission_classes = [permissions.AllowAny]

class TourSearchView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourListSerializer
    permission_classes = [permissions.AllowAny]

class MyToursView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourListSerializer
    permission_classes = [permissions.IsAuthenticated]

class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer
    permission_classes = [permissions.AllowAny]

class TourPriceCalculationView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer
    permission_classes = [permissions.AllowAny]
