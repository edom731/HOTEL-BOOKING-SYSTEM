from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from hotels.models import Room
from .models import Booking, Payment
from .forms import BookingForm, PaymentForm
import uuid


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_available=True)
    hotel = room.hotel

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            nights = (check_out - check_in).days
            total_price = nights * room.price_per_night

            # Check for conflicts
            conflicts = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if conflicts.exists():
                messages.error(request, 'This room is not available for the selected dates.')
                return render(request, 'bookings/create_booking.html', {'form': form, 'room': room, 'hotel': hotel})

            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.total_price = total_price
            booking.save()
            messages.success(request, f'Booking created! Ref: {booking.booking_ref}')
            return redirect('booking_confirm', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form, 'room': room, 'hotel': hotel})


@login_required
def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            method=payment_method,
            status='completed',
            transaction_id='ETH-' + str(uuid.uuid4()).upper()[:10],
            paid_at=timezone.now()
        )
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, f'Payment successful! Your booking {booking.booking_ref} is confirmed.')
        return redirect('booking_detail', pk=booking.pk)

    return render(request, 'bookings/booking_confirm.html', {'booking': booking})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking {booking.booking_ref} has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('my_bookings')
