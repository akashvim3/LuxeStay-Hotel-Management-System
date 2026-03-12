"""LuxeStay URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from pages.sitemaps import StaticViewSitemap, RoomSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'rooms': RoomSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
    path('gallery/', include('gallery.urls')),
    path('blog/', include('blog.urls')),
    path('events/', include('events.urls')),
    path('api/v1/', include('api.urls')),
    
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Note: Static files are automatically served by django.contrib.staticfiles in DEBUG mode
    # from STATICFILES_DIRS. Adding it manually pointing to STATIC_ROOT will fail if collectstatic
    # hasn't been run.
