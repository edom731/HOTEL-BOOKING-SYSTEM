from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Hotel, City, Room


def home(request):
    featured_hotels = Hotel.objects.filter(is_active=True).order_by('-star_rating')[:6]
    cities = City.objects.all()
    total_hotels = Hotel.objects.filter(is_active=True).count()
    features = [
        {'icon': '🔒', 'title': 'Secure Booking', 'desc': 'Your payment and personal data are fully encrypted and protected.'},
        {'icon': '💳', 'title': 'Easy Payment', 'desc': 'Pay via Chapa, TeleBirr, card or cash on arrival.'},
        {'icon': '✅', 'title': 'Instant Confirmation', 'desc': 'Get your booking confirmation instantly.'},
        {'icon': '🌟', 'title': 'Verified Hotels', 'desc': 'All hotels are verified and reviewed by real guests.'},
        {'icon': '📱', 'title': 'Mobile Friendly', 'desc': 'Book from any device — phone, tablet or desktop.'},
        {'icon': '🇪🇹', 'title': 'Ethiopia Focused', 'desc': 'Built specifically for Ethiopian hotels and travelers.'},
    ]
    return render(request, 'hotels/home.html', {
        'featured_hotels': featured_hotels,
        'cities': cities,
        'total_hotels': total_hotels,
        'features': features,
    })


def hotel_list(request):
    hotels = Hotel.objects.filter(is_active=True)
    cities = City.objects.all()

    city_id = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    star_rating = request.GET.get('stars')
    search_q = request.GET.get('q')

    if city_id:
        hotels = hotels.filter(city_id=city_id)
    if min_price:
        hotels = hotels.filter(price_per_night__gte=min_price)
    if max_price:
        hotels = hotels.filter(price_per_night__lte=max_price)
    if star_rating:
        hotels = hotels.filter(star_rating=star_rating)
    if search_q:
        hotels = hotels.filter(
            Q(name__icontains=search_q) |
            Q(city__name__icontains=search_q) |
            Q(description__icontains=search_q)
        )

    return render(request, 'hotels/hotel_list.html', {
        'hotels': hotels,
        'cities': cities,
        'selected_city': city_id,
        'min_price': min_price,
        'max_price': max_price,
        'stars': star_rating,
        'search_q': search_q,
    })


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, is_active=True)
    rooms = hotel.rooms.filter(is_available=True)
    reviews = hotel.reviews.filter(is_approved=True)
    images = hotel.images.all()
    user_reviewed = False
    if request.user.is_authenticated:
        user_reviewed = hotel.reviews.filter(user=request.user).exists()
    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'rooms': rooms,
        'reviews': reviews,
        'images': images,
        'user_reviewed': user_reviewed,
        'star_range': range(1, 6),
    })


def city_hotels(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    hotels = Hotel.objects.filter(city=city, is_active=True)
    return render(request, 'hotels/city_hotels.html', {'city': city, 'hotels': hotels})


@login_required
def add_hotel(request):
    from .forms import HotelForm
    try:
        profile = request.user.profile
        if profile.role not in ['hotel_owner', 'admin'] and not request.user.is_staff:
            messages.error(request, 'Only hotel owners can add hotels.')
            return redirect('home')
    except:
        messages.error(request, 'Please complete your profile first.')
        return redirect('profile')

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, f'Hotel "{hotel.name}" added successfully!')
            return redirect('hotel_detail', pk=hotel.pk)
    else:
        form = HotelForm()
    return render(request, 'hotels/hotel_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_hotel(request, pk):
    from .forms import HotelForm
    hotel = get_object_or_404(Hotel, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hotel updated successfully!')
            return redirect('hotel_detail', pk=hotel.pk)
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'hotels/hotel_form.html', {'form': form, 'hotel': hotel, 'action': 'Edit'})
