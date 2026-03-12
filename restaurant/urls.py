from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='restaurant_menu'),
    path('table-booking/', views.table_booking, name='table_booking'),
    path('order/<int:table_number>/', views.table_order, name='table_order'),
    path('kitchen/', views.kitchen_display, name='kitchen_display'),
    path('inventory/', views.inventory_list, name='inventory_list'),
]
