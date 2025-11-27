from django.urls import path
from . import views

urlpatterns = [
    # Tours CRUD
    path('', views.TourListCreateView.as_view(), name='tour-list-create'),
    path('search/', views.TourSearchView.as_view(), name='tour-search'),
    path('me/', views.MyToursView.as_view(), name='my-tours'),
    path('<int:pk>/', views.TourDetailView.as_view(), name='tour-detail'),
    path('<int:pk>/calculate-price/', views.TourPriceCalculationView.as_view(), name='tour-price-calculation'),
]
