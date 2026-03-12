from rest_framework import serializers
from rooms.models import Room
from restaurant.models import MenuItem

class RoomSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Room
        fields = ['id', 'name', 'slug', 'category_name', 'price_per_night', 'display_price', 'capacity', 'image', 'is_available']

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'category_name', 'price', 'display_price', 'diet_type', 'image', 'is_chef_special']
from bookings.models import RoomBooking, TableReservation
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'loyalty_points', 'preferred_currency']

class RoomBookingSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)
    class Meta:
        model = RoomBooking
        fields = '__all__'

class TableReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableReservation
        fields = '__all__'
