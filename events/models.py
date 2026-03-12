from django.db import models
from django.conf import settings
import uuid

class EventSpace(models.Model):
    """Halls, Terraces, or Lawns for events."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class EventBooking(models.Model):
    """Booking for weddings, parties, etc."""
    
    class EventType(models.TextChoices):
        WEDDING = 'wedding', 'Wedding'
        PARTY = 'party', 'Party'
        CONFERENCE = 'conference', 'Conference'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_bookings')
    space = models.ForeignKey(EventSpace, on_delete=models.CASCADE, related_name='bookings')
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} at {self.space.name} on {self.date}"
