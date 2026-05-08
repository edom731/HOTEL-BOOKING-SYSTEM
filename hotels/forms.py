from django import forms
from .models import Hotel, Room


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'city', 'address', 'description', 'star_rating',
                  'price_per_night', 'thumbnail', 'amenities', 'phone', 'email']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'amenities': forms.TextInput(attrs={'placeholder': 'WiFi, Pool, Gym, Restaurant'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'room_number', 'price_per_night', 'capacity', 'description', 'image', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
