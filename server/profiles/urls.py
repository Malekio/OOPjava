from django.urls import path
from . import views

urlpatterns = [
    # Guide profiles
    path('guides/', views.GuideProfileListView.as_view(), name='guide-list'),
    path('guides/<int:pk>/', views.GuideProfileDetailView.as_view(), name='guide-detail'),
    path('guides/me/', views.GuideProfileMeView.as_view(), name='guide-me'),
    path('guides/<int:pk>/pricing/', views.GuidePricingView.as_view(), name='guide-pricing'),
    
    # Guide certifications
    path('guides/certifications/', views.GuideCertificationListCreateView.as_view(), name='guide-certifications'),
    path('guides/certifications/<int:pk>/', views.GuideCertificationDetailView.as_view(), name='guide-certification-detail'),
    
    # Tourist profiles
    path('tourists/me/', views.TouristProfileMeView.as_view(), name='tourist-me'),
]
