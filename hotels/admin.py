from django.contrib import admin
from .models import City, Hotel, HotelImage, Room

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3

class RoomInline(admin.TabularInline):
    model = Room
    extra = 2

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'star_rating', 'price_per_night', 'owner', 'is_active']
    list_filter = ['city', 'star_rating', 'is_active']
    search_fields = ['name', 'address']
    inlines = [HotelImageInline, RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'room_number', 'room_type', 'price_per_night', 'capacity', 'is_available']
    list_filter = ['room_type', 'is_available', 'hotel']
