from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_type', 'rating', 'title', 'is_verified', 'is_approved', 'created_at')
    list_filter = ('review_type', 'rating', 'is_verified', 'is_approved')
    list_editable = ('is_approved',)
    search_fields = ('title', 'content', 'user__username')
