import google.generativeai as genai
from django.conf import settings
from rooms.models import Room

def get_room_recommendation(user_preferences):
    """
    Uses Gemini AI to suggest rooms based on user preferences.
    Example preferences: {'capacity': 2, 'max_price': 5000, 'style': 'modern'}
    """
    if not settings.GEMINI_API_KEY:
        return Room.objects.filter(is_available=True)[:3]
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    rooms = Room.objects.filter(is_available=True)
    room_list_str = "\n".join([f"- {r.name}: {r.category.name}, Price: ₹{r.price_per_night}, Capacity: {r.capacity}, Description: {r.description[:50]}..." for r in rooms])
    
    prompt = f"""
    You are an AI hotel concierge for LuxeStay. 
    User Preferences: {user_preferences}
    Available Rooms:
    {room_list_str}
    
    Select the best 3 rooms based on the preferences. Return ONLY the names of the rooms, separated by commas.
    If no rooms match perfectly, suggest the closest ones.
    """
    
    try:
        response = model.generate_content(prompt)
        room_names = [name.strip() for name in response.text.split(',')]
        recommended_rooms = Room.objects.filter(name__in=room_names, is_available=True)
        return recommended_rooms
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return rooms[:3]
