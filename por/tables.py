# signup/tables.py
from datetime import datetime,timezone

import django.db.models
import django.utils.html
import django_tables2
import pytz
from django.contrib.auth.models import User
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.db.models import Q,F
from .models import Stations, Station_GPIO_Mappings,RunHeaders,RunDay,RunDetails,Weather
from django.db.models import Sum,Count

from django.conf import settings
myappname = settings.MYAPPNAME
myappname_slash = '/' + settings.MYAPPNAME

class RunDayTable(tables.Table):

    id = tables.Column(verbose_name='')

    def render_weekday(self, value, record):
        vote_count = 0
        data = RunDay.objects.filter(id=record.id)

        return mark_safe('<a href="' + myappname_slash + '/editday?id=' + str(record.id) + '">' + str(value) + '</a>')

    def render_run_status(self, value, record):
        data = RunDay.objects.filter(id=record.id)

        status = ''
        if data[0].run_status == 'Running':
            status = '<span class="stamp stamp-approved">Running</span>'
        elif data[0].run_status == 'Stopped':
            status = '<span class="stamp stamp-declined">Stopped</span>'
        else:
            status = '<span class="stamp stamp-declined">Off</span>'

        return mark_safe(status)

    def render_id(self, value, record):

        data = RunDay.objects.filter(id=record.id)

        if data[0].run_status == 'Running':
            return mark_safe('<a class="btn btn-danger" role="button" href="' + myappname_slash + '/home/?stoprun=Y&stop_run_id=' + str(record.id) + '">' + str('Stop') + '</a>')
        else:
            return('')

    def render_start_time(self, value, record):

        import math
        hour = int(math.floor(value / 100))
        rem = int(value % 100)
        if rem < 10:
            rem = str('0' + str(rem))
        
        ampm = ''
        if (hour < 12):
            ampm = 'AM'
        else:
            ampm = 'PM'

        return(str(hour) + ':' + str(rem)) + ' ' + ampm

    class Meta:
        model = RunDay
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('weekday','start_time','run_status','id')
        attrs = {"class": "table table-striped"}

class RunHeaderTable(tables.Table):
    id = tables.Column(verbose_name='Edit')
    created_by = tables.Column(verbose_name='')

    def render_created_by(self, value, record):
        vote_count = 0
        data = RunHeaders.objects.filter(id=record.id)

        #return mark_safe('<input class="radio optional" type="radio" id="r' + str(record.id) + '" name="r'+ str(record.id) + '" value="' + str(record.id) + '" disabled>')

        return mark_safe('<form id="radioform" method="get"><input class="radio optional" type="radio" id="r' + str(record.id) + '" name="run_id" value="' + str(record.id) + '" onchange="this.form.submit()"></form>')

    def render_id(self, value, record):


        return mark_safe('<a href="' + myappname_slash + '/editrun?run_id=' + str(record.id) + '">' + '<i class="fa fa-edit fa-lg"></i> ' + '</a>')

    def render_run_name(self, value, record):
        vote_count = 0
        data = RunHeaders.objects.filter(id=record.id)

        return mark_safe('<a href="' + myappname_slash + '/home/?run_id=' + str(record.id) + '">' + str(value) + '</a>')

    def render_status(self, value, record):
        data = RunHeaders.objects.filter(id=record.id)

        status = ''
        if data[0].status == 0:
            status = '<span class="stamp stamp-declined">Disabled</span>'
        elif data[0].status == 2:
            status = '<span class="stamp stamp-warning">Raining</span>'
        else:
            status = '<span class="stamp stamp-approved">Enabled</span>'

        return mark_safe(status)

    def render_start_date(self, value, record):

        #fdate = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
        pst = pytz.timezone('Australia/Perth')
        value = value.astimezone(pst)
        if value > datetime.now(pst):
            return mark_safe('<b style="color:red">' + value.strftime('%Y-%m-%d') + '</b>')
            
        return mark_safe('<b>' + value.strftime('%Y-%m-%d')  + '</b>')

    def render_end_date(self, value, record):

        #fdate = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
        pst = pytz.timezone('Australia/Perth')
        value = value.astimezone(pst)

        if value < datetime.now(pst):
            return mark_safe('<b style="color:red">' + value.strftime('%Y-%m-%d') + '</b>')

        return mark_safe('<b>' + value.strftime('%Y-%m-%d') + '</b>')

    def render_last_run(self, value, record):

        #fdate = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
        pst = pytz.timezone('Australia/Perth')
        from sys import platform
        if value:
            value = value.astimezone(pst)
            if platform == "linux" or platform == "linux2":
                return mark_safe(value.strftime('%Y-%m-%d %-I%p'))
            else:
                return mark_safe(value.strftime('%Y-%m-%d %#I%p'))
        else:
            return('')

    class Meta:
        model = RunHeaders
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id','run_name','status','last_run','start_date','end_date')
        attrs = {"class": "table table-striped"}
        sequence = ('created_by','run_name', 'status', 'last_run', 'start_date', 'end_date', 'id',)
        #exclude = ('id',)

class RunDetailsTable(tables.Table):

    id = tables.Column(verbose_name='Edit')
    station_seconds = tables.Column(verbose_name='Minutes / Seconds')
    station_number = tables.Column(accessor='station.station_number')


    def render_station_seconds(self, value, record):
        import math
        minutes_remainder = value % 60
        minutes = value / 60

        if minutes < 1:
            min_sec = str(value) + "s"
        elif minutes_remainder == 0:
            min_sec = str(math.floor(minutes)) + "m"
        else:
            min_sec = str(math.floor(minutes)) + "m " + str(minutes_remainder) + "s"


        return mark_safe('<b>' + min_sec + '</b>')

    def render_id(self, value, record):

        return mark_safe(
            '<a href="' + myappname_slash + '/editdetails?id=' + str(record.id) + '">' + '<i class="fa fa-edit fa-lg"></i> ' + '</a>')

    def render_station_number(self, value, record):
        data = RunDetails.objects.filter(id=record.id).select_related("station")

        return mark_safe('<a href="' + myappname_slash + '/editdetails?id=' + str(record.id) + '">' + str(value) + '</a>')

    def render_run_status(self, value, record):
        data = RunDetails.objects.filter(id=record.id).select_related("station")

        status = ''
        if data[0].run_status == 'Closed':
            status = '<label class ="switch"> <input type = "checkbox" disabled> <span class ="slider round"> </span> </label>'
        else:
            status = '<label class ="switch"> <input type = "checkbox" checked="checked" disabled> <span class ="slider round"> </span> </label>'

        return mark_safe(status)

    class Meta:
        model = RunDetails
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('id','station_number','station_seconds','run_status')
        attrs = {"class": "table table-striped"}

class StationTable(tables.Table):

    station_default_seconds = tables.Column(verbose_name='Default Time (seconds)')
    station_number = tables.Column(verbose_name='Station Number')
    status         = tables.Column(verbose_name='Status')
    id             = tables.Column(verbose_name='GPIO #')

    def render_id(self, value, record):
        data = Stations.objects.filter(id=record.id)
        gpio = Station_GPIO_Mappings.objects.filter(station_id=record.id).first()
        if not gpio:
            gpio_str = ''
        else:
            gpio_str = gpio.station_gpio 

        return mark_safe(str(gpio_str))

    def render_station_number(self, value, record):
        data = Stations.objects.filter(id=record.id)

        return mark_safe('<a href="' + myappname_slash + '/editstation?id=' + str(record.id) + '">' + str(value) + '</a>')

    def render_status(self, value, record):
        data = Stations.objects.filter(id=record.id)

        status = ''
        if data[0].status == 0:   
            return mark_safe('<label class ="switch"><input type="checkbox" id="r' + str(record.id) + '" name="r' + str(record.id) + '" value="' + str(record.id) + '" onchange="handleClick('+ str(record.id) +')"><span class ="slider round"> </span> </label>')
        else:
            return mark_safe('<label class ="switch"><input type="checkbox" id="r' + str(record.id) + '" name="r' + str(record.id) + '" value="' + str(record.id) + '" onchange="handleClick('+ str(record.id) +')" checked="checked"><span class ="slider round"> </span> </label>')

        return mark_safe(status)

    class Meta:
        model = Stations
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('station_number','status','station_default_seconds')
        attrs = {"class": "table table-striped"}

class WeatherTable(tables.Table):

        apparent_t = tables.Column(verbose_name='Temp')
        wind_spd_kmh = tables.Column(verbose_name='Wind Speed')
        wind_dir = tables.Column(verbose_name='Wind Dir')
        rain_trace = tables.Column(verbose_name='Rain')
        local_date_time_full = tables.Column(verbose_name='Date')

        def render_apparent_t(self, value, record):
            return mark_safe(round(value, 1))

        def render_wind_spd_kmh(self, value, record):
            return mark_safe(str(round(value, 0)) + 'km/h')

        def render_gust_kmh(self, value, record):
            return mark_safe(str(round(value, 0)) + 'km/h')

        def render_rain_trace(self, value, record):
            return mark_safe(round(value, 1))

        def render_local_date_time_full(self, value, record):
            v = datetime.strptime(value, '%Y%m%d%H%M%S')
            return mark_safe(v)

        class Meta:
            model = Weather
            template_name = 'django_tables2/bootstrap-responsive.html'
            fields = ('local_date_time_full','apparent_t', 'rain_trace','wind_spd_kmh', 'gust_kmh', 'wind_dir',)
         



class StationGPIOMappingsTable(tables.Table):

    class Meta:
        model = Station_GPIO_Mappings
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-striped"}
