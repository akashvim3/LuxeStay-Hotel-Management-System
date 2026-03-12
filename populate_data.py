"""
LuxeStay - Database Population Script
Run: python manage.py shell < populate_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luxestay.settings')
django.setup()

from accounts.models import User
from rooms.models import RoomCategory, RoomAmenity, Room
from restaurant.models import MenuCategory, MenuItem, RestaurantTable
from pages.models import Testimonial, SpecialOffer
from gallery.models import GalleryCategory, GalleryImage
from blog.models import BlogCategory, BlogPost
from reviews.models import Review

print("Populating LuxeStay Database...")

# ---- Create Superuser ----
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@luxestay.com', 'admin123', first_name='Admin', last_name='LuxeStay', role='admin')
    print("Admin user created (admin/admin123)")

# ---- Room Categories ----
categories_data = [
    {'name': 'Standard', 'slug': 'standard', 'description': 'Comfortable and well-appointed rooms', 'icon': 'fas fa-bed'},
    {'name': 'Deluxe', 'slug': 'deluxe', 'description': 'Spacious rooms with premium amenities', 'icon': 'fas fa-star'},
    {'name': 'Suite', 'slug': 'suite', 'description': 'Luxurious suites with separate living areas', 'icon': 'fas fa-crown'},
]
for cat_data in categories_data:
    RoomCategory.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
print("Room categories created")

# ---- Room Amenities ----
amenities_data = [
    ('Free WiFi', 'fas fa-wifi'), ('Air Conditioning', 'fas fa-snowflake'), ('Mini Bar', 'fas fa-glass-martini'),
    ('Room Service', 'fas fa-concierge-bell'), ('Flat Screen TV', 'fas fa-tv'), ('Safe', 'fas fa-lock'),
    ('King Size Bed', 'fas fa-bed'), ('Sea View', 'fas fa-water'), ('Bathtub', 'fas fa-bath'),
    ('Balcony', 'fas fa-door-open'), ('Coffee Maker', 'fas fa-coffee'), ('Laundry', 'fas fa-tshirt'),
]
amenity_objects = []
for name, icon in amenities_data:
    obj, _ = RoomAmenity.objects.get_or_create(name=name, defaults={'icon': icon})
    amenity_objects.append(obj)
print("Room amenities created")

# ---- Rooms ----
rooms_data = [
    {'name': 'Elegant Standard Room', 'slug': 'elegant-standard', 'category': 'standard', 'description': 'A beautifully appointed room featuring modern amenities, plush bedding, and stunning city views. Perfect for business travelers and couples seeking comfort without compromise.', 'short_description': 'Elegant comfort with city views and modern amenities.', 'price_per_night': 4999, 'capacity': 2, 'size_sqft': 350, 'bed_type': 'Queen Size', 'image': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80', 'is_featured': True, 'rating': 4.5},
    {'name': 'Superior Standard Room', 'slug': 'superior-standard', 'category': 'standard', 'description': 'Our superior standard room offers extra space and enhanced amenities for a truly comfortable stay. Enjoy a peaceful retreat with garden views and premium furnishings.', 'short_description': 'Extra space with garden views and premium furnishings.', 'price_per_night': 5999, 'capacity': 2, 'size_sqft': 400, 'bed_type': 'King Size', 'image': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80', 'is_featured': False, 'rating': 4.3},
    {'name': 'Premium Deluxe Room', 'slug': 'premium-deluxe', 'category': 'deluxe', 'description': 'Spacious deluxe room with panoramic views and premium furnishings. Features a luxurious marble bathroom, walk-in closet, and a private sitting area.', 'short_description': 'Spacious luxury with panoramic views and marble bathroom.', 'price_per_night': 8999, 'discounted_price': 7499, 'capacity': 3, 'size_sqft': 550, 'bed_type': 'King Size', 'image': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80', 'is_featured': True, 'rating': 4.7},
    {'name': 'Grand Deluxe Room', 'slug': 'grand-deluxe', 'category': 'deluxe', 'description': 'Our grand deluxe room features an oversized living space with contemporary design, a rain shower, and breathtaking ocean views from a private balcony.', 'short_description': 'Contemporary design with ocean views and private balcony.', 'price_per_night': 10999, 'discounted_price': 8999, 'capacity': 3, 'size_sqft': 600, 'bed_type': 'King Size', 'image': 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80', 'is_featured': True, 'rating': 4.8},
    {'name': 'Royal Presidential Suite', 'slug': 'presidential-suite', 'category': 'suite', 'description': 'The ultimate luxury experience. Our presidential suite features a private terrace, butler service, jacuzzi, separate living and dining areas, and panoramic ocean views.', 'short_description': 'Ultimate luxury with private terrace and butler service.', 'price_per_night': 18999, 'discounted_price': 14999, 'capacity': 4, 'size_sqft': 900, 'bed_type': 'King Size', 'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80', 'is_featured': True, 'rating': 4.9},
    {'name': 'Honeymoon Suite', 'slug': 'honeymoon-suite', 'category': 'suite', 'description': 'Romantic suite designed for couples featuring a four-poster bed, champagne bar, couples spa bath, rose petal turndown service, and sunset terrace.', 'short_description': 'Romantic suite with champagne bar and sunset terrace.', 'price_per_night': 15999, 'discounted_price': 12999, 'capacity': 2, 'size_sqft': 700, 'bed_type': 'King Size', 'image': 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80', 'is_featured': True, 'rating': 4.9},
]
for room_data in rooms_data:
    cat_slug = room_data.pop('category')
    cat = RoomCategory.objects.get(slug=cat_slug)
    room, created = Room.objects.get_or_create(slug=room_data['slug'], defaults={**room_data, 'category': cat})
    if created:
        room.amenities.set(amenity_objects[:8])
print("Rooms created")

# ---- Menu Categories ----
menu_cats_data = [
    {'name': 'Starters', 'slug': 'starters', 'icon': 'fas fa-pepper-hot', 'order': 1},
    {'name': 'Main Course', 'slug': 'main-course', 'icon': 'fas fa-drumstick-bite', 'order': 2},
    {'name': 'Desserts', 'slug': 'desserts', 'icon': 'fas fa-ice-cream', 'order': 3},
    {'name': 'Beverages', 'slug': 'beverages', 'icon': 'fas fa-glass-martini-alt', 'order': 4},
]
for cat_data in menu_cats_data:
    MenuCategory.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
print("Menu categories created")

# ---- Menu Items ----
menu_items_data = [
    {'name': 'Truffle Mushroom Bruschetta', 'slug': 'truffle-bruschetta', 'category': 'starters', 'description': 'Crispy sourdough topped with sautéed wild mushrooms, truffle oil, and aged parmesan.', 'price': 599, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=400&q=80', 'is_popular': True},
    {'name': 'Grilled Prawn Cocktail', 'slug': 'prawn-cocktail', 'category': 'starters', 'description': 'Jumbo prawns grilled to perfection with cocktail sauce and micro greens.', 'price': 899, 'diet_type': 'non_veg', 'image': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&q=80'},
    {'name': 'Herb-Crusted Lamb Rack', 'slug': 'herb-lamb-rack', 'category': 'main-course', 'description': 'Tender lamb with rosemary crust, truffle mashed potatoes, and red wine jus.', 'price': 1899, 'diet_type': 'non_veg', 'image': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80', 'is_chef_special': True},
    {'name': 'Mediterranean Quinoa Bowl', 'slug': 'quinoa-bowl', 'category': 'main-course', 'description': 'Organic quinoa with roasted vegetables, feta cheese, olives, and lemon tahini dressing.', 'price': 899, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&q=80', 'is_chef_special': True, 'is_popular': True},
    {'name': 'Grilled Atlantic Lobster', 'slug': 'atlantic-lobster', 'category': 'main-course', 'description': 'Fresh lobster tail with garlic herb butter, grilled asparagus, and saffron rice.', 'price': 2499, 'diet_type': 'non_veg', 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80', 'is_chef_special': True},
    {'name': 'Truffle Mushroom Risotto', 'slug': 'mushroom-risotto', 'category': 'main-course', 'description': 'Creamy arborio rice with wild mushrooms, black truffle shavings, and parmesan.', 'price': 1199, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=400&q=80', 'is_popular': True},
    {'name': 'Chocolate Lava Cake', 'slug': 'chocolate-lava', 'category': 'desserts', 'description': 'Warm Belgian chocolate cake with molten center, vanilla ice cream, and berry coulis.', 'price': 499, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&q=80', 'is_popular': True},
    {'name': 'Tiramisu', 'slug': 'tiramisu', 'category': 'desserts', 'description': 'Classic Italian dessert with espresso-soaked ladyfingers and mascarpone cream.', 'price': 449, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&q=80'},
    {'name': 'Signature Craft Cocktail', 'slug': 'craft-cocktail', 'category': 'beverages', 'description': 'Our mixologist\'s special creation with premium spirits and fresh ingredients.', 'price': 699, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400&q=80'},
    {'name': 'Premium Wine Selection', 'slug': 'premium-wine', 'category': 'beverages', 'description': 'Curated selection of fine wines from renowned vineyards worldwide.', 'price': 999, 'diet_type': 'veg', 'image': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400&q=80'},
]
for item_data in menu_items_data:
    cat_slug = item_data.pop('category')
    cat = MenuCategory.objects.get(slug=cat_slug)
    MenuItem.objects.get_or_create(slug=item_data['slug'], defaults={**item_data, 'category': cat})
print("Menu items created")

# ---- Restaurant Tables ----
for i in range(1, 16):
    location = 'Terrace' if i > 12 else 'Outdoor' if i > 8 else 'Indoor'
    capacity = 6 if i % 5 == 0 else 4 if i % 2 == 0 else 2
    RestaurantTable.objects.get_or_create(table_number=i, defaults={'capacity': capacity, 'location': location})
print("Restaurant tables created")

# ---- Testimonials ----
testimonials_data = [
    {'name': 'Rajesh Kumar', 'designation': 'Business Executive', 'content': 'An absolutely magnificent experience! The rooms are breathtaking, the staff is incredibly attentive, and the food is out of this world. LuxeStay has set a new standard for luxury.', 'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80', 'rating': 5, 'order': 1},
    {'name': 'Priya Sharma', 'designation': 'Travel Blogger', 'content': 'Our honeymoon at LuxeStay was pure magic. The suite was romantic, the restaurant dinner was phenomenal, and every detail was perfect. We\'ll never forget this experience!', 'avatar': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80', 'rating': 5, 'order': 2},
    {'name': 'Michael Chen', 'designation': 'International Tourist', 'content': 'The attention to detail at LuxeStay is remarkable. From the welcome drink to the personalized room setup, everything was curated to perfection. Highly recommended!', 'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80', 'rating': 5, 'order': 3},
    {'name': 'Anita Desai', 'designation': 'Corporate Manager', 'content': 'Hosted a corporate retreat here and it exceeded all expectations. The conference facilities are world-class, the food was outstanding, and the team building activities were perfect.', 'avatar': 'https://images.unsplash.com/photo-1494790108755-2616b3cd0c63?w=100&q=80', 'rating': 5, 'order': 4},
]
for test_data in testimonials_data:
    Testimonial.objects.get_or_create(name=test_data['name'], defaults=test_data)
print("Testimonials created")

# ---- Special Offers ----
offers_data = [
    {'title': 'Summer Getaway Package', 'description': '3 nights stay with complimentary breakfast, spa treatment, and airport transfers.', 'discount_percentage': 30, 'image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80', 'code': 'SUMMER30'},
    {'title': 'Honeymoon Paradise', 'description': 'Suite upgrade, champagne dinner, couples spa, and romantic turndown service included.', 'discount_percentage': 25, 'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80', 'code': 'LOVE25'},
    {'title': 'Weekend Escape', 'description': 'Enjoy a luxurious weekend with dining credits, pool access, and late checkout.', 'discount_percentage': 15, 'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&q=80', 'code': 'WEEKEND15'},
]
for offer_data in offers_data:
    SpecialOffer.objects.get_or_create(title=offer_data['title'], defaults=offer_data)
print("Special offers created")

# ---- Gallery ----
gallery_cats = [
    {'name': 'Rooms', 'slug': 'rooms'},
    {'name': 'Dining', 'slug': 'dining'},
    {'name': 'Amenities', 'slug': 'amenities'},
    {'name': 'Events', 'slug': 'events'},
]
for cat_data in gallery_cats:
    GalleryCategory.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)

gallery_images = [
    ('Luxury Suite', 'rooms', 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80'),
    ('Deluxe Room', 'rooms', 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80'),
    ('Presidential Suite', 'rooms', 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80'),
    ('Fine Dining Hall', 'dining', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80'),
    ('Restaurant Terrace', 'dining', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80'),
    ('Infinity Pool', 'amenities', 'https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&q=80'),
    ('Spa & Wellness', 'amenities', 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80'),
    ('Grand Lobby', 'amenities', 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80'),
    ('Wedding Setup', 'events', 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?w=800&q=80'),
]
from events.models import EventSpace

# ---- Event Spaces ----
event_spaces_data = [
    {
        'name': 'The Royal Grand Ballroom',
        'slug': 'grand-ballroom',
        'description': 'A magnificent, pillar-less ballroom with 20ft high ceilings, crystal chandeliers, and regal decor. Perfectly suited for grand weddings, gala dinners, and large-scale corporate events.',
        'capacity': 600,
        'price_per_hour': 15000,
        'image': 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?w=800&q=80',
        'is_available': True
    },
    {
        'name': 'Elite Business Centre',
        'slug': 'business-centre',
        'description': 'A state-of-the-art corporate facility featuring ergonomic seating, high-speed connectivity, and the latest audio-visual technology for important board meetings and executive retreats.',
        'capacity': 120,
        'price_per_hour': 8000,
        'image': 'https://images.unsplash.com/photo-1431540015161-0bf868a2d407?w=800&q=80',
        'is_available': True
    },
    {
        'name': 'Skyline Rooftop Lounge',
        'slug': 'rooftop-lounge',
        'description': 'An open-air venue offering breathtaking 360-degree city views. Ideal for cocktail parties, social mixers, and vibrant evening celebrations under the stars.',
        'capacity': 200,
        'price_per_hour': 12000,
        'image': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&q=80',
        'is_available': True
    },
]
for space_data in event_spaces_data:
    EventSpace.objects.get_or_create(slug=space_data['slug'], defaults=space_data)
print("Event spaces created")

print("\nDatabase populated successfully!")
print("Admin login: admin / admin123")
print("Visit: http://127.0.0.1:8000")
