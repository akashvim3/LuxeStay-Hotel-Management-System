from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EventSpace, EventBooking
from django.utils import timezone

def event_list(request):
    spaces = EventSpace.objects.filter(is_available=True)
    return render(request, 'events/event_list.html', {'spaces': spaces})

@login_required
def book_event(request, slug):
    space = get_object_or_404(EventSpace, slug=slug)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        guests = request.POST.get('guests')
        event_type = request.POST.get('event_type')
        
        # Simple validation
        if not all([date, start_time, end_time, guests, event_type]):
            messages.error(request, "Please fill all required fields.")
        else:
            booking = EventBooking.objects.create(
                user=request.user,
                space=space,
                event_type=event_type,
                date=date,
                start_time=start_time,
                end_time=end_time,
                guests=guests,
                total_amount=space.price_per_hour * 4  # Default 4 hours
            )
            messages.success(request, f"Event booking request sent! We will contact you shortly for confirmation.")
            return redirect('dashboard')
            
    return render(request, 'events/book_event.html', {'space': space, 'event_types': EventBooking.EventType.choices})
