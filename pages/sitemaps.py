from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from rooms.models import Room
from blog.models import BlogPost

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'contact', 'room_list', 'restaurant_menu', 'gallery', 'blog_list']

    def location(self, item):
        return reverse(item)

class RoomSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Room.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.updated_at

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
