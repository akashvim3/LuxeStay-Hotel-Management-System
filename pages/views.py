from django.shortcuts import render, redirect
from django.contrib import messages
from rooms.models import Room
from restaurant.models import MenuItem
from reviews.models import Review
from blog.models import BlogPost
from .models import Testimonial, SpecialOffer, ContactMessage, Newsletter
from bookings.models import RoomBooking
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta


from events.models import EventSpace

def home(request):
    featured_rooms = Room.objects.filter(is_featured=True, is_available=True)[:6]
    chef_specials = MenuItem.objects.filter(is_chef_special=True, is_available=True)[:4]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    special_offers = SpecialOffer.objects.filter(is_active=True)[:3]
    recent_reviews = Review.objects.filter(is_approved=True)[:5]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    event_spaces = EventSpace.objects.filter(is_available=True)[:3]
    
    context = {
        'featured_rooms': featured_rooms,
        'chef_specials': chef_specials,
        'testimonials': testimonials,
        'special_offers': special_offers,
        'recent_reviews': recent_reviews,
        'latest_posts': latest_posts,
        'event_spaces': event_spaces,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    testimonials = Testimonial.objects.filter(is_active=True)[:4]
    return render(request, 'pages/about.html', {'testimonials': testimonials})


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'Your message has been sent successfully! We\'ll get back to you soon.')
        return redirect('contact')
    return render(request, 'pages/contact.html')


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email:
            Newsletter.objects.get_or_create(email=email)
            messages.success(request, 'Thank you for subscribing to our newsletter!')
    return redirect('home')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Simple Rule-based Fallback (can be replaced by Gemini)
            response_text = ""
            
            if 'room' in user_message or 'book' in user_message or 'stay' in user_message:
                response_text = "🛏️ We have luxurious Standard, Deluxe, and Suite rooms available. Would you like to explore our rooms or check availability?"
            elif 'restaurant' in user_message or 'food' in user_message or 'menu' in user_message:
                response_text = "🍽️ Our restaurant offers a world-class menu. You can view our digital menu or reserve a table."
            elif 'price' in user_message or 'cost' in user_message:
                response_text = "💰 Our rooms start from ₹4,999. Visit our Rooms page for detailed pricing."
            elif 'contact' in user_message or 'phone' in user_message:
                response_text = "📞 You can reach us at +91 98765 43210 or email info@luxestay.com."
            elif 'hello' in user_message or 'hi' in user_message:
                response_text = "👋 Hello! Welcome to LuxeStay. How can I assist you today?"
            else:
                # Placeholder for Gemini AI Logic
                # import google.generativeai as genai
                # genai.configure(api_key=settings.GEMINI_API_KEY)
                # model = genai.GenerativeModel('gemini-pro')
                # response = model.generate_content(user_message)
                # response_text = response.text
                response_text = "🤔 I'd be happy to help! You can ask me about room bookings, our restaurant, pricing, or contact details."

            return JsonResponse({'reply': response_text})
        except Exception as e:
            return JsonResponse({'reply': "I'm sorry, I'm having trouble processing your request right now."}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def dashboard_analytics(request):
    """Admin analytics dashboard with Chart.js data."""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Access denied. Staff only.")
        return redirect('home')
    
    # Last 30 days bookings
    last_month = timezone.now() - timedelta(days=30)
    bookings_data = RoomBooking.objects.filter(created_at__gte=last_month).values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')
    
    # Revenue by Room Category
    revenue_data = RoomBooking.objects.filter(is_paid=True).values('room__category__name').annotate(total=Sum('total_amount'))
    
    # Popular Dishes
    popular_dishes = MenuItem.objects.filter(total_orders__gt=0).order_by('-total_orders')[:5]
    
    context = {
        'total_bookings': RoomBooking.objects.count(),
        'total_revenue': RoomBooking.objects.filter(is_paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'pending_bookings': RoomBooking.objects.filter(status='pending').count(),
        'chart_labels': json.dumps([b['created_at__date'].strftime('%b %d') for b in bookings_data]),
        'chart_data': json.dumps([b['count'] for b in bookings_data]),
        'revenue_labels': json.dumps([r['room__category__name'] for r in revenue_data]),
        'revenue_data': json.dumps([float(r['total']) for r in revenue_data]),
        'popular_dishes': popular_dishes,
    }
    return render(request, 'pages/dashboard_analytics.html', context)
