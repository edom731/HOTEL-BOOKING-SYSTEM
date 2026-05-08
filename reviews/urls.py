from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:hotel_id>/', views.add_review, name='add_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
]
