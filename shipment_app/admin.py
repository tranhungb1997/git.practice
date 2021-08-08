from django.contrib import admin
from shipment_app import models


@admin.register(models.ContainerType)
class ContainerTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'size', 'type_name')
    exclude = ('slug',)


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'country_name', 'seaport_name')
    exclude = ('code',)


@admin.register(models.Routing)
class RoutingAdmin(admin.ModelAdmin):
    list_display = ('id', 'orgin_place', 'destination_place')


@admin.register(models.ShipmentInfo)
class ShipmentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'routing', 'start_date')


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'shipment_info')
