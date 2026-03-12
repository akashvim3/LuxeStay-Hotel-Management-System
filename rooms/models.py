from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class RoomCategory(models.Model):
    """Room categories: Standard, Deluxe, Suite, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-bed')
    
    class Meta:
        verbose_name_plural = 'Room Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class RoomAmenity(models.Model):
    """Amenities available in rooms."""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fas fa-check')
    
    class Meta:
        verbose_name_plural = 'Room Amenities'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Room(models.Model):
    """Individual room model."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=2)
    size_sqft = models.PositiveIntegerField(default=300)
    bed_type = models.CharField(max_length=100, default='King Size')
    amenities = models.ManyToManyField(RoomAmenity, blank=True)
    image = models.URLField(max_length=500, blank=True, help_text='Unsplash image URL')
    image_file = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price_per_night']
    
    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'slug': self.slug})
    
    @property
    def display_price(self):
        return self.discounted_price if self.discounted_price else self.price_per_night
    
    @property
    def discount_percentage(self):
        if self.discounted_price and self.discounted_price < self.price_per_night:
            return int(((self.price_per_night - self.discounted_price) / self.price_per_night) * 100)
        return 0
    
    @property
    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        return self.image or 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800'

    def check_availability(self, check_in, check_out):
        """Checks if the room is available for the given dates."""
        from bookings.models import RoomBooking
        # If the room itself is marked as unavailable, return False
        if not self.is_available:
            return False
            
        # Check for overlapping bookings
        overlapping_bookings = RoomBooking.objects.filter(
            room=self,
            status__in=['pending', 'confirmed', 'checked_in'],
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        return not overlapping_bookings.exists()

    def get_price_for_date_range(self, check_in, check_out):
        """Calculates the total price for a date range, considering seasonal adjustments."""
        from datetime import timedelta
        total_price = 0
        current_date = check_in
        while current_date < check_out:
            # Check for seasonal pricing for this specific date
            seasonal = SeasonalPricing.objects.filter(
                room=self,
                start_date__lte=current_date,
                end_date__gte=current_date
            ).first()
            
            if seasonal:
                total_price += seasonal.price
            else:
                total_price += self.display_price
                
            current_date += timedelta(days=1)
        return total_price


class SeasonalPricing(models.Model):
    """Special pricing for holidays or peak seasons."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seasonal_prices')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Seasonal Pricing'
        ordering = ['start_date']

    def __str__(self):
        return f"{self.name} for {self.room.name}"


class RoomImage(models.Model):
    """Gallery images for rooms."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.URLField(max_length=500, blank=True)
    image_file = models.ImageField(upload_to='rooms/gallery/', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.room.name}"
    
    @property
    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        return self.image or ''
