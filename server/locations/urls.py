from django.urls import path
from . import views

urlpatterns = [
    path('', views.WilayaListView.as_view(), name='wilaya-list'),
    path('<int:pk>/', views.WilayaDetailView.as_view(), name='wilaya-detail'),
    path('<int:pk>/guides/', views.WilayaGuidesView.as_view(), name='wilaya-guides'),
    path('<int:pk>/tours/', views.WilayaToursView.as_view(), name='wilaya-tours'),
]
