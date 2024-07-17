from django.urls import path
from . import views

urlpatterns = [
    path('add_shift/', views.add_shift, name='add_shift'),
    path('shift_list/', views.shift_list, name='shift_list'),
    path('book_shift/<int:shift_id>/', views.book_shift, name='book_shift'),
    path('api/get_shifts/', views.api_get_shifts, name='api_get_shifts'),
    path('bookings/', views.booking_list, name='bookings'),  # New URL for bookings
    path('api/book_shift/', views.api_book_shift, name='api_book_shift'),
    path('', views.home, name='home'),  # Home page

]
