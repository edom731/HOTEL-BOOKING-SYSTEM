from django.contrib import admin
from .models import Booking, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_ref', 'user', 'room', 'check_in', 'check_out', 'total_price', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['booking_ref', 'user__username']
    inlines = [PaymentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'method', 'status', 'paid_at']
    list_filter = ['status', 'method']
