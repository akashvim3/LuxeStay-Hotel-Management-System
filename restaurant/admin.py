from django.contrib import admin
from .models import MenuCategory, MenuItem, RestaurantTable, InventoryItem, TableOrder


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'diet_type', 'is_chef_special', 'is_available', 'is_popular', 'rating')
    list_filter = ('category', 'diet_type', 'is_chef_special', 'is_available', 'is_popular')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_available', 'is_chef_special', 'is_popular')


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'location', 'is_available', 'qr_code')
    list_filter = ('location', 'is_available', 'capacity')
    list_editable = ('is_available',)

    def qr_code(self, obj):
        from django.utils.html import format_html
        # In production, use your actual domain
        url = f"http://127.0.0.1:8000/restaurant/order/{obj.table_number}/"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={url}"
        return format_html('<img src="{}" width="50" height="50" />', qr_url)
    qr_code.short_description = 'Table QR'


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'min_stock_level', 'is_low_stock')
    list_editable = ('quantity', 'min_stock_level')


@admin.register(TableOrder)
class TableOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total_amount', 'created_at')
