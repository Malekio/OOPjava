from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import TouristProfile, GuideProfile, GuideAvailability, GuideCertification


@admin.register(TouristProfile)
class TouristProfileAdmin(admin.ModelAdmin):
    """Admin interface for Tourist profiles"""

    list_display = [
        "user",
        "nationality",
        "preferred_language",
        "created_at",
        "profile_picture_preview",
    ]
    list_filter = ["nationality", "preferred_language", "created_at"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "nationality",
    ]
    readonly_fields = ["created_at", "updated_at", "profile_picture_preview"]
    ordering = ["-created_at"]

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Profile Details",
            {"fields": ("bio", "date_of_birth", "nationality", "preferred_language")},
        ),
        ("Profile Picture", {"fields": ("profile_picture", "profile_picture_preview")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def profile_picture_preview(self, obj):
        """Display profile picture thumbnail"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 25px;" />',
                obj.profile_picture.url,
            )
        return "No image"

    profile_picture_preview.short_description = "Profile Picture"


class GuideCertificationInline(admin.TabularInline):
    """Inline admin for Guide Certifications"""

    model = GuideCertification
    extra = 1
    fields = ("title", "document", "is_verified")


class GuideAvailabilityInline(admin.TabularInline):
    """Inline admin for Guide Availability"""

    model = GuideAvailability
    extra = 1
    fields = ("date", "time_slot", "is_available")


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    """Admin interface for Guide profiles"""

    list_display = [
        "user",
        "years_of_experience",
        "verification_status",
        "average_rating",
        "coverage_areas_count",
        "created_at",
        "profile_picture_preview",
    ]
    list_filter = [
        "verification_status",
        "years_of_experience",
        "created_at",
        "coverage_areas",
    ]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "bio",
    ]
    readonly_fields = ["created_at", "updated_at", "profile_picture_preview"]
    filter_horizontal = ["coverage_areas"]
    inlines = [GuideCertificationInline, GuideAvailabilityInline]
    ordering = ["-created_at"]

    fieldsets = (
        ("User Information", {"fields": ("user",)}),
        (
            "Professional Details",
            {"fields": ("bio", "years_of_experience", "languages")},
        ),
        (
            "Verification Status",
            {
                "fields": ("verification_status", "verification_notes"),
                "classes": ("collapse",),
            },
        ),
        (
            "Coverage & Pricing",
            {
                "fields": (
                    "coverage_areas",
                    "half_day_price",
                    "full_day_price",
                    "extra_hour_price",
                )
            },
        ),
        ("Profile Picture", {"fields": ("profile_picture", "profile_picture_preview")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def profile_picture_preview(self, obj):
        """Display profile picture thumbnail"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 25px;" />',
                obj.profile_picture.url,
            )
        return "No image"

    profile_picture_preview.short_description = "Profile Picture"

    def coverage_areas_count(self, obj):
        """Display number of coverage areas"""
        return obj.coverage_areas.count()

    coverage_areas_count.short_description = "Coverage Areas"

    actions = ["verify_guides", "unverify_guides"]

    def verify_guides(self, request, queryset):
        """Action to verify selected guides"""
        updated = queryset.update(verification_status="verified")
        self.message_user(request, f"{updated} guides were verified successfully.")

    verify_guides.short_description = "Verify selected guides"

    def unverify_guides(self, request, queryset):
        """Action to unverify selected guides"""
        updated = queryset.update(verification_status="pending")
        self.message_user(request, f"{updated} guides were set to pending.")

    unverify_guides.short_description = "Set to pending"


@admin.register(GuideCertification)
class GuideCertificationAdmin(admin.ModelAdmin):
    """Admin interface for Guide Certifications"""

    list_display = ["title", "guide", "is_verified", "created_at"]
    list_filter = ["is_verified", "created_at"]
    search_fields = [
        "title",
        "guide__user__username",
        "guide__user__first_name",
        "guide__user__last_name",
    ]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Certification Details", {"fields": ("guide", "title", "document")}),
        ("Verification Status", {"fields": ("is_verified",)}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    actions = ["verify_certifications", "unverify_certifications"]

    def verify_certifications(self, request, queryset):
        """Action to verify selected certifications"""
        updated = queryset.update(is_verified=True)
        self.message_user(
            request, f"{updated} certifications were verified successfully."
        )

    verify_certifications.short_description = "Verify selected certifications"

    def unverify_certifications(self, request, queryset):
        """Action to unverify selected certifications"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} certifications were unverified.")

    unverify_certifications.short_description = "Unverify selected certifications"


@admin.register(GuideAvailability)
class GuideAvailabilityAdmin(admin.ModelAdmin):
    """Admin interface for Guide Availability"""

    list_display = ["guide", "date", "time_slot", "is_available"]
    list_filter = ["date", "time_slot", "is_available"]
    search_fields = [
        "guide__user__username",
        "guide__user__first_name",
        "guide__user__last_name",
    ]
    ordering = ["-date"]
    date_hierarchy = "date"

    fieldsets = (
        ("Guide & Date", {"fields": ("guide", "date")}),
        ("Availability Details", {"fields": ("time_slot", "is_available")}),
    )
