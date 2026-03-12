from django.shortcuts import render
from .models import GalleryCategory, GalleryImage

def gallery_view(request):
    categories = GalleryCategory.objects.all()
    images = GalleryImage.objects.select_related('category').all()
    
    category_filter = request.GET.get('category')
    if category_filter:
        images = images.filter(category__slug=category_filter)
    
    context = {
        'categories': categories,
        'images': images,
        'selected_category': category_filter,
    }
    return render(request, 'gallery/gallery.html', context)
