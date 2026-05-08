from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/city/<int:city_id>/', views.city_hotels, name='city_hotels'),
    path('hotels/add/', views.add_hotel, name='add_hotel'),
    path('hotels/<int:pk>/edit/', views.edit_hotel, name='edit_hotel'),
]
