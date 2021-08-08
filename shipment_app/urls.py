from django.urls import path
from shipment_app import views
from django.views.generic import TemplateView

app_name = 'shipment_app'
urlpatterns = [
    path('container-type/json', views.container_type_json, name='container_type_json'),
    path('city/json', views.city_json, name='city_json'),
    path('', TemplateView.as_view(template_name='shipment/home.html'), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('booking/<int:id>', views.Booking.as_view(), name='booking'),
    path('booking-confirm/', views.BookingConfirm.as_view(), name='booking_confirm'),
    path('booking/success/', TemplateView.as_view(template_name='shipment/booking-success.html'), name='booking_success'),
]