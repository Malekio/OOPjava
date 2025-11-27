from rest_framework import serializers
from .models import Wilaya

class WilayaSerializer(serializers.ModelSerializer):
    """
    Serializer for Wilaya (Algerian administrative divisions)
    """
    class Meta:
        model = Wilaya
        fields = ['id', 'code', 'name_ar', 'name_en', 'name_fr']

class WilayaDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Wilaya with additional statistics
    """
    total_guides = serializers.SerializerMethodField()
    total_tours = serializers.SerializerMethodField()
    
    class Meta:
        model = Wilaya
        fields = ['id', 'code', 'name_ar', 'name_en', 'name_fr', 'total_guides', 'total_tours']
    
    def get_total_guides(self, obj):
        return obj.guides.filter(verification_status='verified').count()
    
    def get_total_tours(self, obj):
        return obj.tour_set.filter(status='active').count()
