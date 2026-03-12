from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from bookings.models import RoomBooking, TableReservation


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to LuxeStay! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    room_bookings = RoomBooking.objects.filter(user=request.user).order_by('-created_at')[:5]
    table_reservations = TableReservation.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'room_bookings': room_bookings,
        'table_reservations': table_reservations,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    context = {}
    if request.user.is_admin_user or request.user.is_superuser:
        from rooms.models import Room
        from restaurant.models import MenuItem
        from django.db.models import Sum, Count
        from django.db.models.functions import TruncDate
        from django.utils import timezone
        import datetime
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        
        booking_stats = RoomBooking.objects.filter(created_at__gte=thirty_days_ago) \
            .annotate(date=TruncDate('created_at')) \
            .values('date') \
            .annotate(count=Count('id')) \
            .order_by('date')
            
        context.update({
            'total_rooms': Room.objects.count(),
            'total_bookings': RoomBooking.objects.count(),
            'total_reservations': TableReservation.objects.count(),
            'total_menu_items': MenuItem.objects.count(),
            'total_revenue': RoomBooking.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'recent_bookings': RoomBooking.objects.order_by('-created_at')[:10],
            'recent_reservations': TableReservation.objects.order_by('-created_at')[:10],
            'chart_data_dates': [s['date'].strftime('%Y-%m-%d') for s in booking_stats],
            'chart_data_counts': [s['count'] for s in booking_stats],
        })
        return render(request, 'accounts/admin_dashboard.html', context)
    
    context.update({
        'room_bookings': RoomBooking.objects.filter(user=request.user).order_by('-created_at'),
        'table_reservations': TableReservation.objects.filter(user=request.user).order_by('-created_at'),
    })
    return render(request, 'accounts/customer_dashboard.html', context)
def set_preference(request):
    """View to set currency/language preferences."""
    pref_type = request.GET.get('type')
    value = request.GET.get('value')
    referer = request.META.get('HTTP_REFERER', 'home')
    
    if pref_type == 'currency':
        if request.user.is_authenticated:
            request.user.preferred_currency = value
            request.user.save()
        request.session['currency'] = value
        messages.success(request, f"Currency changed to {value}.")
    
    elif pref_type == 'language':
        if request.user.is_authenticated:
            request.user.preferred_language = value
            request.user.save()
        request.session['language'] = value
        messages.success(request, f"Language changed to {value}.")
        
    return redirect(referer)
