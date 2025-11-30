from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from profiles.models import TouristProfile, GuideProfile


class TouristProfileInline(admin.StackedInline):
    """Inline admin for TouristProfile"""

    model = TouristProfile
    can_delete = False
    verbose_name_plural = "Tourist Profile"
    extra = 0
    fields = (
        "bio",
        "date_of_birth",
        "nationality",
        "preferred_language",
        "profile_picture",
    )


class GuideProfileInline(admin.StackedInline):
    """Inline admin for GuideProfile"""

    model = GuideProfile
    can_delete = False
    verbose_name_plural = "Guide Profile"
    extra = 0
    fields = (
        "bio",
        "years_of_experience",
        "languages",
        "is_verified",
        "verification_date",
        "profile_picture",
        "coverage_areas",
        "half_day_price",
        "full_day_price",
        "extra_hour_price",
    )
    filter_horizontal = ("coverage_areas",)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin with profile inlines"""

    inlines = [TouristProfileInline, GuideProfileInline]

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)

    def user_type(self, obj):
        """Display user type based on profile"""
        if hasattr(obj, "tourist_profile"):
            return "Tourist"
        elif hasattr(obj, "guide_profile"):
            return "Guide"
        return "Admin"

    user_type.short_description = "User Type"

    def get_inline_instances(self, request, obj=None):
        """Only show relevant profile inline based on user type"""
        inlines = []
        if obj:
            if hasattr(obj, "tourist_profile"):
                inlines = [TouristProfileInline(self.model, self.admin_site)]
            elif hasattr(obj, "guide_profile"):
                inlines = [GuideProfileInline(self.model, self.admin_site)]
        return inlines
