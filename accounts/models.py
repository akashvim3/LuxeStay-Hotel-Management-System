from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model with role-based access."""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'
        STAFF = 'staff', 'Staff'
        CUSTOMER = 'customer', 'Customer'
    
    class Currency(models.TextChoices):
        INR = 'INR', 'Indian Rupee (₹)'
        USD = 'USD', 'US Dollar ($)'
        EUR = 'EUR', 'Euro (€)'
        GBP = 'GBP', 'British Pound (£)'
        
    class Language(models.TextChoices):
        EN = 'en', 'English'
        HI = 'hi', 'Hindi'
        FR = 'fr', 'French'
        ES = 'es', 'Spanish'
        
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    preferred_currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.INR)
    preferred_language = models.CharField(max_length=10, choices=Language.choices, default=Language.EN)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_loyalty_member(self):
        return self.loyalty_points > 100

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @property
    def is_staff_member(self):
        return self.role == self.Role.STAFF

    class Meta:
        ordering = ['-created_at']
