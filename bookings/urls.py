from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:room_id>/', views.create_booking, name='create_booking'),
    path('confirm/<int:pk>/', views.booking_confirm, name='booking_confirm'),
    path('detail/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]
