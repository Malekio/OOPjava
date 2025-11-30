"""
URL configuration for DZ-TourGuide server project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({"status": "healthy", "message": "DZ-TourGuide API is running"})


@api_view(["GET"])
@permission_classes([AllowAny])
def metrics(request):
    """Basic metrics endpoint"""
    from accounts.models import User
    from profiles.models import GuideProfile
    from tours.models import Tour
    from bookings.models import Booking

    metrics_data = {
        "total_users": User.objects.count(),
        "total_guides": GuideProfile.objects.filter(
            verification_status="verified"
        ).count(),
        "total_tours": Tour.objects.filter(status="active").count(),
        "total_bookings": Booking.objects.count(),
        "completed_bookings": Booking.objects.filter(status="completed").count(),
    }

    return Response(metrics_data)


urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("v1/auth/", include("accounts.urls")),
    path("v1/profiles/", include("profiles.urls")),
    path("v1/tours/", include("tours.urls")),
    path("v1/bookings/", include("bookings.urls")),
    path("v1/reviews/", include("reviews.urls")),
    path("v1/wilayas/", include("locations.urls")),
    path("v1/messaging/", include("messaging.urls")),
    # Health and metrics
    path("v1/health/", health_check, name="health-check"),
    path("v1/metrics/", metrics, name="metrics"),
]

# Customize admin site
admin.site.site_header = "DZ-TourGuide Administration"
admin.site.site_title = "DZ-TourGuide Admin Portal"
admin.site.index_title = "Welcome to DZ-TourGuide Administration"
admin.site.site_url = "/"

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
