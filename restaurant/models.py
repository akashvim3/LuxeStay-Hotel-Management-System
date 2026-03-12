from django.db import models
from django.utils.text import slugify


class MenuCategory(models.Model):
    """Menu categories: Starters, Main Course, Desserts, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-utensils')
    image = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Menu Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MenuItem(models.Model):
    """Individual menu items."""
    
    class DietType(models.TextChoices):
        VEG = 'veg', 'Vegetarian'
        NON_VEG = 'non_veg', 'Non-Vegetarian'
        VEGAN = 'vegan', 'Vegan'
    
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.URLField(max_length=500, blank=True)
    image_file = models.ImageField(upload_to='menu/', blank=True, null=True)
    diet_type = models.CharField(max_length=10, choices=DietType.choices, default=DietType.NON_VEG)
    is_chef_special = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    spice_level = models.PositiveIntegerField(default=1, help_text='1-5 scale')
    prep_time = models.PositiveIntegerField(default=20, help_text='Minutes')
    calories = models.PositiveIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    total_orders = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_chef_special', '-is_popular', 'name']
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def display_price(self):
        return self.discounted_price if self.discounted_price else self.price
    
    @property
    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        return self.image or 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400'
    
    @property
    def diet_badge_class(self):
        return 'badge-veg' if self.diet_type == 'veg' else 'badge-nonveg' if self.diet_type == 'non_veg' else 'badge-vegan'


class RestaurantTable(models.Model):
    """Restaurant tables for reservation."""
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)
    location = models.CharField(max_length=100, default='Indoor', help_text='Indoor, Outdoor, Terrace, etc.')
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['table_number']
    
    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} seats - {self.location})"

    @property
    def get_qr_code_url(self):
        """Returns a URL to a QR code that points to the ordering page."""
        import urllib.parse
        base_url = "https://luxestay.com/restaurant/order/" # Placeholder
        full_url = f"{base_url}{self.table_number}/"
        encoded_url = urllib.parse.quote(full_url)
        return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={encoded_url}"


class InventoryItem(models.Model):
    """Tracking raw materials or drinks stock."""
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=20, default='kg', help_text='kg, liters, units, etc.')
    min_stock_level = models.PositiveIntegerField(default=5)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock_level


class TableOrder(models.Model):
    """Direct ordering from tables (QR Code)."""
    
    class Status(models.TextChoices):
        ORDERED = 'ordered', 'Ordered'
        PREPARING = 'preparing', 'Preparing'
        SERVED = 'served', 'Served'
        PAID = 'paid', 'Paid'

    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(MenuItem, related_name='table_orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order at Table {self.table.table_number} - {self.get_status_display()}"
