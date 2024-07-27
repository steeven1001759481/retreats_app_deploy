# retreat_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('retreats/', views.get_retreats),
    path('book/', views.book_retreat),
    path('booked/', views.get_bookings)
]
