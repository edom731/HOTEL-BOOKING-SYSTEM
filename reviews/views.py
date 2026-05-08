from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hotels.models import Hotel
from .models import Review


@login_required
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id, is_active=True)

    if Review.objects.filter(hotel=hotel, user=request.user).exists():
        messages.warning(request, 'You have already reviewed this hotel.')
        return redirect('hotel_detail', pk=hotel_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if not rating or not comment:
            messages.error(request, 'Please provide both a rating and a comment.')
            return redirect('hotel_detail', pk=hotel_id)
        Review.objects.create(
            hotel=hotel,
            user=request.user,
            rating=int(rating),
            comment=comment,
            is_approved=True
        )
        messages.success(request, 'Thank you for your review!')
    return redirect('hotel_detail', pk=hotel_id)


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    hotel_id = review.hotel.pk
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('hotel_detail', pk=hotel_id)
