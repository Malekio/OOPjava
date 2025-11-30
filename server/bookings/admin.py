from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from django.utils import timezone
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for Bookings"""

    list_display = [
        "id",
        "tourist",
        "tour_title",
        "guide",
        "booking_date",
        "time_slot",
        "status",
        "total_price",
        "group_size",
        "created_at",
    ]
    list_filter = ["status", "time_slot", "booking_date", "created_at", "tour__wilaya"]
    search_fields = [
        "tourist__user__username",
        "tourist__user__first_name",
        "tourist__user__last_name",
        "tour__title",
        "tour__guide__user__username",
    ]
    readonly_fields = ["total_price", "created_at", "updated_at"]
    ordering = ["-created_at"]
    date_hierarchy = "booking_date"

    fieldsets = (
        ("Booking Information", {"fields": ("tourist", "tour")}),
        ("Schedule", {"fields": ("booking_date", "time_slot")}),
        ("Group Details", {"fields": ("group_size", "total_price")}),
        ("Status & Notes", {"fields": ("status", "notes")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def tour_title(self, obj):
        """Display tour title"""
        return obj.tour.title

    tour_title.short_description = "Tour"

    def guide(self, obj):
        """Display guide name"""
        return obj.tour.guide.user.get_full_name() or obj.tour.guide.user.username

    guide.short_description = "Guide"

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        return (
            super()
            .get_queryset(request)
            .select_related("tourist__user", "tour__guide__user", "tour__wilaya")
        )

    actions = [
        "confirm_bookings",
        "reject_bookings",
        "cancel_bookings",
        "complete_bookings",
    ]

    def confirm_bookings(self, request, queryset):
        """Action to confirm selected bookings"""
        updated = queryset.filter(status="pending").update(status="confirmed")
        self.message_user(request, f"{updated} bookings were confirmed successfully.")

    confirm_bookings.short_description = "Confirm selected bookings"

    def reject_bookings(self, request, queryset):
        """Action to reject selected bookings"""
        updated = queryset.filter(status__in=["pending", "confirmed"]).update(
            status="rejected"
        )
        self.message_user(request, f"{updated} bookings were rejected.")

    reject_bookings.short_description = "Reject selected bookings"

    def cancel_bookings(self, request, queryset):
        """Action to cancel selected bookings"""
        updated = queryset.filter(status__in=["pending", "confirmed"]).update(
            status="cancelled"
        )
        self.message_user(request, f"{updated} bookings were cancelled.")

    cancel_bookings.short_description = "Cancel selected bookings"

    def complete_bookings(self, request, queryset):
        """Action to mark selected bookings as completed"""
        today = timezone.now().date()
        updated = queryset.filter(status="confirmed", booking_date__lte=today).update(
            status="completed"
        )
        self.message_user(request, f"{updated} bookings were marked as completed.")

    complete_bookings.short_description = "Mark as completed (past bookings only)"

    def get_list_filter(self, request):
        """Dynamic filters based on user permissions"""
        filters = list(self.list_filter)
        if request.user.is_superuser:
            filters.append("tour__guide__verification_status")
        return filters

    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}

        # Get booking statistics
        total_bookings = self.get_queryset(request).count()
        pending_bookings = self.get_queryset(request).filter(status="pending").count()
        confirmed_bookings = (
            self.get_queryset(request).filter(status="confirmed").count()
        )
        completed_bookings = (
            self.get_queryset(request).filter(status="completed").count()
        )

        extra_context["booking_stats"] = {
            "total": total_bookings,
            "pending": pending_bookings,
            "confirmed": confirmed_bookings,
            "completed": completed_bookings,
        }

        return super().changelist_view(request, extra_context)
