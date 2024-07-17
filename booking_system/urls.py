# booking_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
    path('', RedirectView.as_view(url='/booking/')),  # Redirect root to booking
]
