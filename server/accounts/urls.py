from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('logout/', views.logout_view, name='user-logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User profile endpoints
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
]
