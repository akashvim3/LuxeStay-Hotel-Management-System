from django.shortcuts import render
from .models import MenuCategory, MenuItem


def menu_view(request):
    categories = MenuCategory.objects.filter(is_active=True).prefetch_related('items')
    chef_specials = MenuItem.objects.filter(is_chef_special=True, is_available=True)[:6]
    popular_items = MenuItem.objects.filter(is_popular=True, is_available=True)[:6]
    
    # Filter by diet type
    diet_filter = request.GET.get('diet')
    category_filter = request.GET.get('category')
    
    menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
    
    if diet_filter:
        menu_items = menu_items.filter(diet_type=diet_filter)
    if category_filter:
        menu_items = menu_items.filter(category__slug=category_filter)
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'chef_specials': chef_specials,
        'popular_items': popular_items,
        'selected_diet': diet_filter,
        'selected_category': category_filter,
    }
    return render(request, 'restaurant/menu.html', context)


def table_booking(request):
    return render(request, 'restaurant/table_booking.html')


def table_order(request, table_number):
    """View for QR code table ordering."""
    from .models import RestaurantTable, MenuItem, TableOrder
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    table = get_object_or_404(RestaurantTable, table_number=table_number)
    menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
    
    if request.method == 'POST':
        item_ids = request.POST.getlist('items')
        if not item_ids:
            messages.warning(request, "Please select at least one item.")
        else:
            order = TableOrder.objects.create(table=table)
            order.items.add(*item_ids)
            # Calculate total
            total = sum(item.display_price for item in order.items.all())
            order.total_amount = total
            order.save()
            messages.success(request, f"Order placed for Table {table_number}! Total: ₹{total}")
            return redirect('menu_view')

    return render(request, 'restaurant/table_order.html', {
        'table': table,
        'menu_items': menu_items,
    })


def kitchen_display(request):
    """View for kitchen staff to see active orders."""
    from .models import TableOrder
    if not request.user.is_staff:
        return redirect('home')
    
    active_orders = TableOrder.objects.filter(status__in=['ordered', 'preparing']).order_by('created_at')
    return render(request, 'restaurant/kitchen_display.html', {'orders': active_orders})


def inventory_list(request):
    """View to manage restaurant stock."""
    from .models import InventoryItem
    if not request.user.is_staff:
        return redirect('home')
    
    items = InventoryItem.objects.all()
    return render(request, 'restaurant/inventory.html', {'items': items})
