from rest_framework import routers
from .views import (
    RoomViewSet, MenuItemViewSet, RoomBookingViewSet, 
    TableReservationViewSet, UserViewSet
)

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'menu', MenuItemViewSet)
router.register(r'room-bookings', RoomBookingViewSet)
router.register(r'table-reservations', TableReservationViewSet)
router.register(r'profile', UserViewSet)

urlpatterns = router.urls
