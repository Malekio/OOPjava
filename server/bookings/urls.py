from django.urls import path
from . import views

urlpatterns = [
    # Bookings
    path('', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/status/', views.BookingStatusUpdateView.as_view(), name='booking-status-update'),
    path('<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking-cancel'),
    path('<int:pk>/invoice/', views.BookingInvoiceView.as_view(), name='booking-invoice'),
    path('guide/pending/', views.GuidePendingBookingsView.as_view(), name='guide-pending-bookings'),
    path('tourist/upcoming/', views.TouristUpcomingBookingsView.as_view(), name='tourist-upcoming-bookings'),
    path('calendar/available/', views.GuideAvailabilityCalendarView.as_view(), name='guide-availability-calendar'),
]
