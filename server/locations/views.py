from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Wilaya
from .serializers import WilayaSerializer, WilayaDetailSerializer
from profiles.serializers import GuideProfileListSerializer
from tours.serializers import TourListSerializer


class WilayaListView(generics.ListAPIView):
    """
    List all Algerian wilayas
    """

    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer
    permission_classes = [permissions.AllowAny]


class WilayaDetailView(generics.RetrieveAPIView):
    """
    Get specific wilaya details with statistics
    """

    queryset = Wilaya.objects.all()
    serializer_class = WilayaDetailSerializer
    permission_classes = [permissions.AllowAny]


class WilayaGuidesView(generics.ListAPIView):
    """
    List all guides in a specific wilaya
    """

    serializer_class = GuideProfileListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        wilaya_id = self.kwargs["pk"]
        wilaya = get_object_or_404(Wilaya, id=wilaya_id)
        return wilaya.guides.filter(verification_status="verified").select_related(
            "user"
        )


class WilayaToursView(generics.ListAPIView):
    """
    List all tours in a specific wilaya
    """

    serializer_class = TourListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        wilaya_id = self.kwargs["pk"]
        wilaya = get_object_or_404(Wilaya, id=wilaya_id)
        return wilaya.tour_set.filter(status="active").select_related("guide__user")
