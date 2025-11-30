from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, CustomTourRequestViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(
    r"custom-requests", CustomTourRequestViewSet, basename="custom-requests"
)

urlpatterns = [
    path("", include(router.urls)),
]
