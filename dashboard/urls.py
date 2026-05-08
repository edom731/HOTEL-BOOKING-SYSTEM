from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/rooms/<int:hotel_id>/', views.manage_rooms, name='manage_rooms'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/hotels/', views.manage_hotels, name='manage_hotels'),
]
