from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rooms.models import Room
from .models import RoomBooking, TableReservation
from .forms import RoomBookingForm, TableReservationForm
import uuid

@login_required
def book_room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            
            # Basic validation
            from django.utils import timezone
            if check_in < timezone.now().date():
                messages.error(request, "Check-in date cannot be in the past.")
            elif check_out <= check_in:
                messages.error(request, "Check-out date must be after check-in.")
            elif not room.check_availability(check_in, check_out):
                messages.error(request, "Sorry, this room is already booked for the selected dates.")
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.room = room
                
                # Check for coupon
                coupon_code = request.POST.get('coupon_code')
                if coupon_code:
                    from .models import Coupon
                    from django.utils import timezone
                    coupon = Coupon.objects.filter(
                        code__iexact=coupon_code,
                        active=True,
                        valid_from__lte=timezone.now(),
                        valid_to__gte=timezone.now()
                    ).first()
                    if coupon:
                        booking.coupon = coupon
                        messages.success(request, f"Coupon '{coupon_code}' applied! You saved {coupon.discount_percent}%.")
                    else:
                        messages.warning(request, "Invalid or expired coupon code.")

                booking.calculate_total()
                booking.save()
                messages.success(request, f'Room booking initiated! Please complete your payment.')
                return redirect('pay_booking', booking_id=booking.booking_id)
    else:
        # Check if dates were passed via query params (from availability checker on home page)
        initial_data = {}
        if 'check_in' in request.GET:
            initial_data['check_in'] = request.GET.get('check_in')
        if 'check_out' in request.GET:
            initial_data['check_out'] = request.GET.get('check_out')
        if 'guests' in request.GET:
            initial_data['guests'] = request.GET.get('guests')
            
        form = RoomBookingForm(initial=initial_data)
    
    context = {
        'room': room,
        'form': form,
    }
    return render(request, 'bookings/book_room.html', context)


@login_required
def pay_booking(request, booking_id):
    booking = get_object_or_404(RoomBooking, booking_id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Mocking Stripe Payment
        booking.is_paid = True
        booking.status = 'confirmed'
        booking.payment_id = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        booking.save()
        
        # Add loyalty points (1 point per 100 rupees)
        request.user.loyalty_points += int(booking.total_amount / 100)
        request.user.save()
        
        messages.success(request, f'Payment successful! Your stay is confirmed.')
        return redirect('booking_confirmation', booking_id=booking.booking_id)
        
    return render(request, 'bookings/payment.html', {'booking': booking})


@login_required
def reserve_table(request):
    if request.method == 'POST':
        form = TableReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, f'Table reserved successfully! Reservation ID: {reservation.reservation_id}')
            return redirect('reservation_confirmation', reservation_id=reservation.reservation_id)
    else:
        form = TableReservationForm()
    
    return render(request, 'bookings/reserve_table.html', {'form': form})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(RoomBooking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})


@login_required
def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(TableReservation, reservation_id=reservation_id, user=request.user)
    return render(request, 'bookings/reservation_confirmation.html', {'reservation': reservation})


@login_required
def my_bookings(request):
    room_bookings = RoomBooking.objects.filter(user=request.user).select_related('room')
    table_reservations = TableReservation.objects.filter(user=request.user)
    context = {
        'room_bookings': room_bookings,
        'table_reservations': table_reservations,
    }
    return render(request, 'bookings/my_bookings.html', context)
