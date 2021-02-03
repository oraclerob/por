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
        ordering = ('station_number',)

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
        ordering = ('station',)


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
