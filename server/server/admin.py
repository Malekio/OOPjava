"""
Custom admin site with enhanced dashboard
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count, Sum
from accounts.models import User
from profiles.models import GuideProfile
from tours.models import Tour
from bookings.models import Booking
from reviews.models import Review


class DZTourGuideAdminSite(AdminSite):
    """Custom admin site for DZ-TourGuide"""

    site_header = "DZ-TourGuide Administration"
    site_title = "DZ-TourGuide Admin Portal"
    index_title = "Welcome to DZ-TourGuide Administration"

    def index(self, request, extra_context=None):
        """
        Display the admin index page with custom statistics
        """
        extra_context = extra_context or {}

        # Gather platform statistics
        try:
            stats = {
                "total_users": User.objects.count(),
                "verified_guides": GuideProfile.objects.filter(
                    is_verified=True
                ).count(),
                "active_tours": Tour.objects.filter(status="active").count(),
                "total_bookings": Booking.objects.count(),
                "pending_reviews": Review.objects.filter(is_approved=False).count(),
                "total_revenue": Booking.objects.filter(status="completed").aggregate(
                    total=Sum("total_amount")
                )["total"]
                or 0,
            }
            extra_context.update(stats)
        except Exception as e:
            # Handle case where database tables don't exist yet
            pass

        return super().index(request, extra_context)


# Create instance of custom admin site
admin_site = DZTourGuideAdminSite(name="dztourguide_admin")
