from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).select_related('category', 'author')
    categories = BlogCategory.objects.all()
    featured = posts.filter(is_featured=True)[:3]
    
    category_filter = request.GET.get('category')
    if category_filter:
        posts = posts.filter(category__slug=category_filter)
    
    context = {
        'posts': posts,
        'categories': categories,
        'featured_posts': featured,
        'selected_category': category_filter,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    related_posts = BlogPost.objects.filter(
        category=post.category, is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/blog_detail.html', context)
