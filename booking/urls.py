from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('add_shift/', views.add_shift, name='add_shift'),
    path('shift_list/', views.shift_list, name='shift_list'),
    path('book_shift/<int:shift_id>/', views.book_shift, name='book_shift'),
    path('api/get_shifts/', views.api_get_shifts, name='api_get_shifts'),
    path('bookings/', views.booking_list, name='bookings'), 
    path('api/book_shift/', views.api_book_shift, name='api_book_shift'),
    path('', login_view, name='login'),  
    path('booking/booked_shifts/', views.booked_shifts, name='booked_shifts'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('home', views.home, name='home'),
    path('request_shift_swap/<int:shift_id>/<int:to_employee_id>/', request_shift_swap, name='request_shift_swap'),
    path('manage_shift_swaps/', manage_shift_swaps, name='manage_shift_swaps'),
    path('approve_swap/<int:swap_id>/', approve_swap, name='approve_swap'),
    path('deny_swap/<int:swap_id>/', deny_swap, name='deny_swap'),



]
