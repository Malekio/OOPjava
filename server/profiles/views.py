from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TouristProfile, GuideProfile, GuideCertification
from .serializers import (
    TouristProfileSerializer,
    GuideProfileSerializer,
    GuideProfileListSerializer,
    GuideProfileUpdateSerializer,
    GuideCertificationSerializer,
    GuidePricingSerializer
)
from .permissions import IsOwnerOrReadOnly, IsGuideOwner
from .filters import GuideProfileFilter

class GuideProfileListView(generics.ListAPIView):
    """
    List all verified guides with filtering and search
    """
    queryset = GuideProfile.objects.filter(verification_status='verified').select_related('user')
    serializer_class = GuideProfileListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GuideProfileFilter
    search_fields = ['user__first_name', 'user__last_name', 'bio', 'languages']
    ordering_fields = ['average_rating', 'total_reviews', 'created_at']
    ordering = ['-average_rating']

class GuideProfileDetailView(generics.RetrieveAPIView):
    """
    Get specific guide details
    """
    queryset = GuideProfile.objects.filter(verification_status='verified').select_related('user')
    serializer_class = GuideProfileSerializer
    permission_classes = [permissions.AllowAny]

class GuideProfileMeView(generics.RetrieveUpdateAPIView):
    """
    Get and update current guide's profile
    """
    serializer_class = GuideProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsGuideOwner]
    
    def get_object(self):
        return self.request.user.guide_profile
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
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
        guide_id = self.kwargs['pk']
        return GuideProfile.objects.get(id=guide_id, verification_status='verified')
