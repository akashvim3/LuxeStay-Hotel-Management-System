from rest_framework import viewsets
from rooms.models import Room
from restaurant.models import MenuItem
from bookings.models import RoomBooking, TableReservation
from django.contrib.auth import get_user_model
from .serializers import RoomSerializer, MenuItemSerializer, RoomBookingSerializer, TableReservationSerializer, UserSerializer

User = get_user_model()

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class RoomBookingViewSet(viewsets.ModelViewSet):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return RoomBooking.objects.all()
        return RoomBooking.objects.filter(user=self.request.user)

class TableReservationViewSet(viewsets.ModelViewSet):
    queryset = TableReservation.objects.all()
    serializer_class = TableReservationSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return TableReservation.objects.all()
        return TableReservation.objects.filter(user=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
