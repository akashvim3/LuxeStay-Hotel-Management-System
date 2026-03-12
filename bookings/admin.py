from django.contrib import admin
from .models import RoomBooking, TableReservation


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'room', 'check_in', 'check_out', 'status', 'total_amount', 'is_paid')
    list_filter = ('status', 'is_paid', 'check_in')
    search_fields = ('booking_id', 'user__username', 'room__name')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    list_editable = ('status', 'is_paid')


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'user', 'date', 'time', 'guests', 'status')
    list_filter = ('status', 'date')
    search_fields = ('reservation_id', 'user__username')
    readonly_fields = ('reservation_id', 'created_at')
    list_editable = ('status',)
