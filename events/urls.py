from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('book/<slug:slug>/', views.book_event, name='book_event'),
]
