from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from hotels.models import Hotel, Room
from bookings.models import Booking
from reviews.models import Review
from hotels.forms import HotelForm, RoomForm


def owner_or_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            profile = request.user.profile
            if profile.role not in ['hotel_owner', 'admin'] and not request.user.is_staff:
                messages.error(request, 'Access denied. Owner or Admin privileges required.')
                return redirect('home')
        except:
            messages.error(request, 'Profile not found.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            try:
                if request.user.profile.role != 'admin':
                    messages.error(request, 'Access denied. Admin privileges required.')
                    return redirect('home')
            except:
                messages.error(request, 'Access denied.')
                return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@login_required
def dashboard(request):
    try:
        profile = request.user.profile
        role = profile.role
    except:
        role = 'customer'

    if role == 'admin' or request.user.is_staff:
        return redirect('admin_dashboard')
    elif role == 'hotel_owner':
        return redirect('owner_dashboard')
    else:
        return redirect('my_bookings')


@owner_or_admin_required
def owner_dashboard(request):
    if request.user.is_staff:
        hotels = Hotel.objects.all()
    else:
        hotels = Hotel.objects.filter(owner=request.user)
    hotel_ids = hotels.values_list('id', flat=True)
    bookings = Booking.objects.filter(room__hotel__id__in=hotel_ids).order_by('-created_at')[:10]
    total_revenue = sum(b.total_price for b in Booking.objects.filter(room__hotel__id__in=hotel_ids, status='confirmed'))
    return render(request, 'dashboard/owner_dashboard.html', {
        'hotels': hotels,
        'recent_bookings': bookings,
        'total_revenue': total_revenue,
    })


@owner_or_admin_required
def manage_rooms(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if not request.user.is_staff and hotel.owner != request.user:
        messages.error(request, 'You can only manage your own hotel rooms.')
        return redirect('owner_dashboard')
    rooms = hotel.rooms.all()
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            messages.success(request, f'Room {room.room_number} added successfully!')
            return redirect('manage_rooms', hotel_id=hotel_id)
    else:
        form = RoomForm()
    return render(request, 'dashboard/manage_rooms.html', {'hotel': hotel, 'rooms': rooms, 'form': form})


@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_hotels = Hotel.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = sum(b.total_price for b in Booking.objects.filter(status='confirmed'))
    recent_bookings = Booking.objects.order_by('-created_at')[:15]
    recent_users = User.objects.order_by('-date_joined')[:10]
    return render(request, 'dashboard/admin_dashboard.html', {
        'total_users': total_users,
        'total_hotels': total_hotels,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'recent_users': recent_users,
    })


@admin_required
def manage_users(request):
    users = User.objects.select_related('profile').order_by('-date_joined')
    return render(request, 'dashboard/manage_users.html', {'users': users})


@admin_required
def manage_hotels(request):
    hotels = Hotel.objects.select_related('city', 'owner').order_by('-created_at')
    return render(request, 'dashboard/manage_hotels.html', {'hotels': hotels})
