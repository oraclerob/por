from django.contrib import admin

# Register your models here.
from .models import Station_GPIO_Mappings,Stations,RunHeaders,RunDay,RunDetails,Weather,Settings

class StationsAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in Stations._meta.get_fields() if field.name != "id"]
    list_display = ['station_number', 'station_default_seconds']

class Station_GPIO_MappingsAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in Station_GPIO_Mappings._meta.get_fields() if field.name != "id"]
    list_display = ['station', 'station_gpio']

class RunHeadersAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in RunHeaders._meta.get_fields() if field.name != "id"]
    list_display = ['run_name','start_date','end_date']

class RunDetailsAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in RunDetails._meta.get_fields() if field.name != "id"]
    list_display = ['run','run_id', 'station_id', 'station_gpio_id', 'station_seconds']

    # def get_station_gpio(self, obj):
    #     return obj.Station_GPIO_MappingsAdmin.station_gpio

class RunDayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RunDay._meta.get_fields() if field.name != "id"]

class WeatherAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Weather._meta.get_fields() if field.name != "id"]

class SettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Settings._meta.get_fields() if field.name != "id"]

admin.site.register(Stations, StationsAdmin)
admin.site.register(Station_GPIO_Mappings,Station_GPIO_MappingsAdmin)
admin.site.register(RunHeaders,RunHeadersAdmin)
admin.site.register(RunDay,RunDayAdmin)
admin.site.register(RunDetails,RunDetailsAdmin)
admin.site.register(Weather,WeatherAdmin)
admin.site.register(Settings,SettingsAdmin)
