from django.urls import path
from . import views

urlpatterns = [
    path('room/<slug:slug>/', views.book_room, name='book_room'),
    path('table/', views.reserve_table, name='reserve_table'),
    path('confirm/<uuid:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('pay/<uuid:booking_id>/', views.pay_booking, name='pay_booking'),
    path('reservation/<uuid:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
