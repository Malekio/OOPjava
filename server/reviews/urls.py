from django.urls import path
from . import views

urlpatterns = [
    # Reviews
    path('tours/<int:tour_id>/reviews/', views.TourReviewListView.as_view(), name='tour-reviews'),
    path('guides/<int:guide_id>/reviews/', views.GuideReviewListView.as_view(), name='guide-reviews'),
    path('bookings/<int:booking_id>/review/', views.BookingReviewCreateView.as_view(), name='booking-review-create'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]
