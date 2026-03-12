from django.db import models
from django.conf import settings


class Review(models.Model):
    """User reviews for rooms and restaurant."""
    
    class ReviewType(models.TextChoices):
        ROOM = 'room', 'Room'
        RESTAURANT = 'restaurant', 'Restaurant'
        GENERAL = 'general', 'General'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    review_type = models.CharField(max_length=20, choices=ReviewType.choices, default=ReviewType.GENERAL)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    rating = models.PositiveIntegerField(default=5, help_text='Rating 1-5')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.rating}★)"
    
    @property
    def star_range(self):
        return range(self.rating)
    
    @property
    def empty_star_range(self):
        return range(5 - self.rating)
