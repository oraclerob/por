from decimal import Decimal
from datetime import datetime
from django.contrib import admin

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.safestring import mark_safe


class Stations(models.Model):
    station_number          = models.CharField(unique=True,max_length=255,error_messages={'unique':"This station has already been registered."})
    station_default_seconds = models.BigIntegerField(default=0)
    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)
    status                  = models.IntegerField(default=0)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return self.station_number

    class Meta:
        verbose_name_plural = "Stations"

class Station_GPIO_Mappings(models.Model):
    station                 = models.ForeignKey(Stations, on_delete=models.CASCADE)
    station_gpio            = models.BigIntegerField(unique=True,default=0)
    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return str(self.station)

    class Meta:
        verbose_name_plural = "Station_GPIO_Mappings"

class RunHeaders(models.Model):
    run_name                = models.CharField(unique=True, max_length=255, error_messages={'unique': "This run name has already been registered."})
    start_date              = models.DateTimeField(default=datetime.now, blank=True)
    end_date                = models.DateTimeField(default=datetime.now, blank=True)
    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)
    status                  = models.IntegerField(default=0)
    last_run                = models.DateTimeField(default=datetime.now, null=True, blank=True)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return str(self.run_name)

    class Meta:
        verbose_name_plural = "RunHeaders"

class RunDay(models.Model):
    run                     = models.ForeignKey(RunHeaders,on_delete=models.CASCADE)
    weekday                 = models.CharField(max_length=255)
    start_time              = models.BigIntegerField(default=0)
    run_status              = models.CharField(max_length=255,blank=True)
    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return str(self.run)

    class Meta:
        verbose_name_plural = "RunDay"

class RunDetails(models.Model):
    run                     = models.ForeignKey(RunHeaders,on_delete=models.CASCADE)
    station                 = models.ForeignKey(Stations,on_delete=models.CASCADE)
    station_gpio            = models.ForeignKey(Station_GPIO_Mappings,  to_field='station_gpio', on_delete=models.CASCADE)
    station_seconds         = models.BigIntegerField(default=0)
    run_status              = models.CharField(max_length=255,blank=True)
    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return str(self.run)

    class Meta:
        verbose_name_plural = "RunDetails"


class Weather(models.Model):
    sort_order              = models.BigIntegerField(default=0,null=True,blank=True)
    name                    = models.CharField(max_length=255,null=True,blank=True)
    local_date_time_full    = models.CharField(max_length=255, null=True,blank=True)
    apparent_t              = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    delta_t                 = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    gust_kmh                = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    air_temp                = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    press                   = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    rain_trace              = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    rel_hum                 = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    wind_spd_kmh            = models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True)
    wind_dir                = models.CharField(max_length=255, null=True,blank=True)

    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)



    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return str(self.name)

    class Meta:
        verbose_name_plural = "Weather"

class Settings(models.Model):
    rain_detection          = models.BigIntegerField(default=0,null=True,blank=True)
    bom_url                 = models.CharField(max_length=255, null=True,blank=True)
    rain_threshold          = models.BigIntegerField(default=0,null=True,blank=True)

    created_by              = models.BigIntegerField(default=0)
    creation_date           = models.DateTimeField(default=datetime.now, blank=True)
    last_updated_by         = models.BigIntegerField(default=0)
    last_update_date        = models.DateTimeField(default=datetime.now, blank=True)



    def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
        return str(self.rain_detection)

    class Meta:
        verbose_name_plural = "Settings"


# Create your models here.

# class Venues(models.Model):
#     venue_name        = models.CharField(unique=True,max_length=255,error_messages={'unique':"This venue has already been registered."})
#     venue_type        = models.CharField(max_length=30,blank=True, null=True)
#     formatted_address = models.CharField(max_length=255)
#     google_maps_url   = models.CharField(max_length=255)
#     lattitude         = models.CharField(max_length=255)
#     longitude         = models.CharField(max_length=255)
#     website_url       = models.CharField(max_length=255)
#     place_id          = models.CharField(max_length=255,blank=True, null=True)
#     created_by        = models.BigIntegerField(default=0)
#     creation_date     = models.DateTimeField(default=datetime.now, blank=True)
#     last_updated_by   = models.BigIntegerField(default=0)
#     last_update_date  = models.DateTimeField(default=datetime.now, blank=True)
#
#     def __str__(self):  # __str__ for Python 3, __unicode__ for Python 2
#         return self.venue_name
#
#     class Meta:
#         verbose_name_plural = "Venues"
#
#
# class Drinks(models.Model):
#         venue      = models.ForeignKey(Venues, on_delete=models.CASCADE)
#         drink_name = models.CharField(max_length=255, error_messages={'unique':"This drink has already been registered."})
#         price      = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal(0))
#         drink_size = models.CharField(max_length=30)
#         comments   = models.CharField(max_length=255,default=None, blank=True, null=True)
#         hh_price   = models.DecimalField(decimal_places=2,max_digits=10,default=Decimal(0), blank=True, null=True, verbose_name="Happy Hour Price")
#         hh_days    = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="Happy Hour Days")
#         hh_time_start = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="Happy Hour Start Time")
#         hh_time_end = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="Happy Hour End Time")
#         created_by  = models.BigIntegerField(default=0)
#         creation_date = models.DateTimeField(default=datetime.now, blank=True)
#         last_updated_by = models.BigIntegerField(default=0)
#         last_update_date = models.DateTimeField(default=datetime.now, blank=True)
#
#         def __str__(self):
#             return self.drink_name
#
#         class Meta:
#             unique_together = (('venue', 'drink_name','drink_size'))
#             verbose_name_plural = "Drinks"
#
#
# def my_function(self):
#     # Return some calculated value based on the entry
#     return mark_safe("""<div id="topic" class="upvote">
#                             <a class="upvote"></a>
#                             <span class="count">0</span>
#                             <a class="downvote"></a>
#                             <a class="star"></a>
#                         </div>
#                      """)
#
# class Votes(models.Model):
#     username         = models.ForeignKey(User,db_column='username_id',on_delete=models.CASCADE,error_messages={'unique':"You cannot vote up more than once per drink!"})
#     vote_count       = models.BigIntegerField()
#     points_count     = models.BigIntegerField()
#     vote_date        = models.DateTimeField()
#     venue            = models.ForeignKey(Venues,db_column='venue_id',on_delete=models.CASCADE)
#     drink            = models.ForeignKey(Drinks,db_column='drink_id', on_delete=models.CASCADE,null=True,blank = True)
#     created_by       = models.BigIntegerField(default=0)
#     creation_date    = models.DateTimeField(default=datetime.now, blank=True)
#     last_updated_by  = models.BigIntegerField(default=0)
#     last_update_date = models.DateTimeField(default=datetime.now, blank=True)
#
#     def __str__(self):
#         return str(self.username)
#
#     class Meta:
#         unique_together = ('venue', 'drink', 'username', 'created_by',)
#         ordering = ('vote_count',)
#         verbose_name_plural = "Votes"
#
#
# class DrinkBrands(models.Model):
#     drink_name = models.CharField(unique=True,max_length=255)
#     drink_type = models.CharField(max_length=255)
#     created_by       = models.BigIntegerField(default=0)
#     creation_date    = models.DateTimeField(default=datetime.now, blank=True)
#     last_updated_by  = models.BigIntegerField(default=0)
#     last_update_date = models.DateTimeField(default=datetime.now, blank=True)
#
#     def __str__(self):
#         return self.drink_name
#
#     class Meta:
#         ordering = ('drink_name',)
#         verbose_name_plural = "DrinkBrand"





