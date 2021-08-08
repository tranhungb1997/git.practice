from django.db import models
from django.utils.text import slugify

from user.models import UserCustom


class City(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    country_code = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    seaport_code = models.CharField(max_length=50)
    seaport_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.code = slugify(self.country_code + "-" + self.seaport_code)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.country_name + '(' + self.seaport_code + ')'

    class Meta:
        db_table = 'city_tbl'


class Routing(models.Model):
    id = models.AutoField(primary_key=True)
    orgin_place = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='orgin_set')
    destination_place = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name='destination_set')

    def __str__(self):
        return self.orgin_place.country_name + "(" + self.orgin_place.seaport_code + ")->" + self.destination_place.country_name + "(" + self.destination_place.seaport_code + ")"

    class Meta:
        db_table = 'routing_tbl'


class ContainerType(models.Model):
    slug = models.SlugField(primary_key=True)
    size = models.IntegerField()
    type_name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.size) + "-" + self.type_name)
        super(ContainerType, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'container_type_tbl'


class ShipmentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    routing = models.ForeignKey(to=Routing, on_delete=models.CASCADE)
    type_container = models.ForeignKey(to=ContainerType, on_delete=models.CASCADE)
    start_date = models.DateField()
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'shipment_info_tbl'


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    shipment_info = models.ForeignKey(to=ShipmentInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserCustom, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)
    insert_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking_tbl'
