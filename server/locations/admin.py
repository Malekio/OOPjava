from django.contrib import admin
from .models import Wilaya


@admin.register(Wilaya)
class WilayaAdmin(admin.ModelAdmin):
    """Admin interface for Algerian Wilayas"""

    list_display = ["code", "name_en", "name_ar", "name_fr", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["code", "name_en", "name_ar", "name_fr"]
    readonly_fields = ["created_at"]
    ordering = ["code"]

    fieldsets = (
        ("Basic Information", {"fields": ("code",)}),
        ("Names (Multi-language)", {"fields": ("name_ar", "name_en", "name_fr")}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return super().get_queryset(request).select_related()
