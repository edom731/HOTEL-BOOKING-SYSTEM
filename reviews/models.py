from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['hotel', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} ({self.rating}/5)"
