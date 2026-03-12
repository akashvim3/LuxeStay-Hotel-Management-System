from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Room, RoomCategory, RoomAmenity, SeasonalPricing


def room_list(request):
    rooms = Room.objects.select_related('category').prefetch_related('amenities').filter(is_available=True)
    categories = RoomCategory.objects.all()
    amenities_list = RoomAmenity.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    guests = request.GET.get('guests')
    capacity = request.GET.get('capacity') or guests
    search = request.GET.get('search')
    
    # Date-based availability filtering
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if check_in and check_out:
        from bookings.models import RoomBooking
        # Find rooms that are NOT available for these dates
        taken_room_ids = RoomBooking.objects.filter(
            status__in=['pending', 'confirmed', 'checked_in'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
        
        rooms = rooms.exclude(id__in=taken_room_ids)
    
    if category_slug:
        rooms = rooms.filter(category__slug=category_slug)
    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)
    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)
    if search:
        rooms = rooms.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    
    # Advanced Filtering
    selected_amenities_ids = request.GET.getlist('amenity')
    sort_by = request.GET.get('sort')
    
    if selected_amenities_ids:
        for amenity_id in selected_amenities_ids:
            rooms = rooms.filter(amenities__id=amenity_id)
            
    if sort_by == 'price_low':
        rooms = rooms.order_by('price_per_night')
    elif sort_by == 'price_high':
        rooms = rooms.order_by('-price_per_night')
    elif sort_by == 'popular':
        rooms = rooms.order_by('-id') # Placeholder for popular logic
    
    context = {
        'rooms': rooms,
        'categories': categories,
        'amenities_list': amenities_list,
        'selected_category': category_slug,
        'selected_amenities': [int(a) for a in selected_amenities_ids],
        'selected_sort': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
    }
    return render(request, 'rooms/room_list.html', context)


def room_detail(request, slug):
    room = get_object_or_404(
        Room.objects.select_related('category').prefetch_related('amenities', 'gallery_images'),
        slug=slug
    )
    # AI Recommendation Logic:
    from .ai_utils import get_room_recommendation
    user_prefs = {
        'category': room.category.name,
        'capacity': room.capacity,
        'style': room.description,
        'price': str(room.price_per_night)
    }
    recommended_rooms = get_room_recommendation(user_prefs)
    if not recommended_rooms:
        recommended_rooms = Room.objects.filter(category=room.category, is_available=True).exclude(id=room.id)[:3]
    
    context = {
        'room': room,
        'related_rooms': recommended_rooms,
    }
    return render(request, 'rooms/room_detail.html', context)
