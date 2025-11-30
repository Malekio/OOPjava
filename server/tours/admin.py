from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    """Admin interface for Tours"""

    list_display = [
        "title",
        "guide",
        "wilaya",
        "status",
        "duration_hours",
        "price",
        "max_group_size",
        "bookings_count",
        "image_preview",
        "created_at",
    ]
    list_filter = ["status", "wilaya", "duration_hours", "created_at"]
    search_fields = [
        "title",
        "description",
        "guide__user__username",
        "guide__user__first_name",
        "guide__user__last_name",
        "wilaya__name_en",
        "tags",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "slug",
        "price",
        "image_preview",
        "bookings_count",
    ]
    filter_horizontal = []
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Information", {"fields": ("guide", "title", "description", "slug")}),
        (
            "Location & Duration",
            {
                "fields": (
                    "wilaya",
                    "meeting_point",
                    "latitude",
                    "longitude",
                    "duration_hours",
                )
            },
        ),
        ("Group & Pricing", {"fields": ("max_group_size", "price")}),
        (
            "Services",
            {
                "fields": ("included_services", "excluded_services"),
                "classes": ("collapse",),
            },
        ),
        ("Status & Visibility", {"fields": ("status", "tags")}),
        ("Media", {"fields": ("image", "image_preview")}),
        ("Statistics", {"fields": ("bookings_count",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def image_preview(self, obj):
        """Display tour image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="60" style="border-radius: 5px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Tour Image"

    def bookings_count(self, obj):
        """Display number of bookings for this tour"""
        if hasattr(obj, "booking_count"):
            return obj.booking_count
        return obj.bookings.count()

    bookings_count.short_description = "Total Bookings"

    def get_queryset(self, request):
        """Optimize queryset with related data and annotations"""
        return (
            super()
            .get_queryset(request)
            .select_related("guide__user", "wilaya")
            .annotate(booking_count=Count("bookings"))
        )

    actions = ["activate_tours", "deactivate_tours", "mark_as_draft"]

    def activate_tours(self, request, queryset):
        """Action to activate selected tours"""
        updated = queryset.update(status="active")
        self.message_user(request, f"{updated} tours were activated successfully.")

    activate_tours.short_description = "Activate selected tours"

    def deactivate_tours(self, request, queryset):
        """Action to deactivate selected tours"""
        updated = queryset.update(status="inactive")
        self.message_user(request, f"{updated} tours were deactivated.")

    deactivate_tours.short_description = "Deactivate selected tours"

    def mark_as_draft(self, request, queryset):
        """Action to mark selected tours as draft"""
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} tours were marked as draft.")

    mark_as_draft.short_description = "Mark as draft"

    def save_model(self, request, obj, form, change):
        """Custom save to handle automatic price calculation"""
        super().save_model(request, obj, form, change)

    class Media:
        css = {"all": ("admin/css/tours.css",)}
        js = ("admin/js/tours.js",)
