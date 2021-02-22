#import _mysql
import threading

import dateutil.tz.tz

import RPi.GPIO as GPIO
import os
import sys
from sys import platform
if platform == "linux" or platform == "linux2":
    sys.path.append('/python/Web')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
elif platform == "win32":
    sys.path.append('C:\Python\myprojects\Web')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import time
import pytz
from _datetime import datetime, timezone
from django.db import connection

import requests
import json
import django
from django.db.models import Q
django.setup()

if __name__ == '__main__':
    from por.por.models import Stations, Station_GPIO_Mappings, RunDay, RunDetails, RunHeaders,Weather,Settings
else:
    from .models import Stations, Station_GPIO_Mappings, RunDay, RunDetails, RunHeaders,Weather,Settings


class ReticEngine():

    master = Station_GPIO_Mappings.objects.select_related('station').filter(station__station_number='Master')

    if master:
        MASTER_STATION_GPIO = master[0].station_gpio
    else:
        MASTER_STATION_GPIO = 0

    def __init__(self, *args, **kwargs):
        None

    def start_new_thread(function):
        def decorator(*args, **kwargs):
            t = threading.Thread(target=function, args=args, kwargs=kwargs)
            t.daemon = False
            t.start()
            return t

        return decorator

    @staticmethod
    def get_stations():
            stations = Station_GPIO_Mappings.objects.all().select_related('station').filter(~Q(station__station_number='Master')).filter(Q(station__status=1))
            return stations

    @staticmethod
    @start_new_thread
    def runOneDB(station, seconds):
        GPIO.setmode(GPIO.BCM)

        try:
            station = Station_GPIO_Mappings.objects.select_related('station').filter(station__station_number=station)
            ReticEngine.openCloseValvesDB(station[0].station.station_number,station[0].station_gpio, seconds)

            # perform a bit of cleanup
            GPIO.cleanup()
            connection.close()

        except:
            print("An Error occured OR user stopped routine...!!!")
            # Shut all valves...
            ReticEngine.closeValvesDB()
            GPIO.cleanup()
            connection.close()
            raise

    @staticmethod
    @start_new_thread
    def stopOneDB(station_number):
        GPIO.setmode(GPIO.BCM)

        try:
            station = Station_GPIO_Mappings.objects.select_related('station').filter(station__station_number=station_number)

            GPIO.setup(station[0].station_gpio, GPIO.OUT)
            print("Close valve: " + str(station_number) + " | " + str(station[0].station_gpio))
            time.sleep(0.1)
            GPIO.output(station[0].station_gpio, GPIO.BOARD)

            # perform a bit of cleanup
            GPIO.cleanup()
            connection.close()

        except:
            print("An Error occured OR user stopped routine...!!!")
            # Shut all valves...
            ReticEngine.closeValvesDB()
            GPIO.cleanup()
            connection.close()
            raise



    @staticmethod
    @start_new_thread
    def runAllFromDB(seconds = None):
        for i in  ReticEngine.get_stations():
            ReticEngine.openCloseValvesDB(i.station.station_number,i.station_gpio ,i.station.station_default_seconds if seconds == None else seconds)

    @staticmethod
    @start_new_thread
    def stopRun(run_day_id):
        pst = pytz.timezone('Australia/Perth')
        now = datetime.now(pst)
        rd = RunDay.objects.filter(id=run_day_id)

        ReticEngine.closeValvesDB()

        for s in rd:
            s.last_updated_by = 0
            s.last_update_date = now
            s.run_status = 'Stopped'
            s.save()

    @staticmethod
    def runCycleFromDB(run_details,run_day_id):
        pst = pytz.timezone('Australia/Perth')
        now = datetime.now(pst)
        h = RunHeaders.objects.filter(id=run_details[0].run_id)
        for s in h:
            s.last_updated_by = 0
            s.last_update_date = now
            s.run_status = 'Running'
            s.save()

        for i in run_details:
            rh = RunHeaders.objects.filter(id=i.run_id)
            st = Stations.objects.filter(id=i.station_id)
            if st[0].status == 0:
                print("Skipping station not enabled: ", st[0].station_number)
                continue
            rd = RunDay.objects.filter(id=run_day_id)
            if rd[0].run_status == 'Stopped':
                if (ReticEngine.MASTER_STATION_GPIO != 0):
                    print("Closing Master Station GPIO: ", ReticEngine.MASTER_STATION_GPIO)
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(ReticEngine.MASTER_STATION_GPIO, GPIO.OUT)
                    GPIO.output(ReticEngine.MASTER_STATION_GPIO, GPIO.LOW)  # Close valve

                GPIO.setmode(GPIO.BCM)
                GPIO.setup(i.station_gpio_id, GPIO.OUT)
                GPIO.output(i.station_gpio_id, GPIO.LOW)  # Close valve
                print("Closed Station:", st[0].station_number, 'GPIO: ', i.station_gpio_id)

                i.last_updated_by = 0
                i.last_update_date = now
                i.run_status = 'Closed'
                i.save()
            else:
                ReticEngine.openCloseValvesDB(st[0].station_number, i.station_gpio_id, i.station_seconds,rh,i)

        for s in h:
            s.last_updated_by = 0
            s.last_update_date = now
            s.run_status = ''
            s.save()


    @staticmethod
    def openCloseValvesDB(station, gpio, seconds, run_header=None,run_details = None, run_day=None):

         GPIO.setmode(GPIO.BCM)

         if (ReticEngine.MASTER_STATION_GPIO !=0):
             print("Opening Master Station GPIO: ", ReticEngine.MASTER_STATION_GPIO, " for ", seconds, " seconds")
             GPIO.setup(ReticEngine.MASTER_STATION_GPIO, GPIO.OUT)
             GPIO.output(ReticEngine.MASTER_STATION_GPIO, GPIO.HIGH)  # Open valve

         print("Opening Station:", station, 'GPIO: ', gpio, " for ", seconds, " seconds")
         time.sleep(2.0)
         GPIO.setup(gpio, GPIO.OUT)
         print("Setup valve: " + str(gpio))
         GPIO.output(gpio, GPIO.HIGH)  # Open valve
         print("Opened Station:", station, 'GPIO: ', gpio, " for ", seconds, " seconds")

         pst = pytz.timezone('Australia/Perth')
         now = datetime.now(pst)

         if run_details:
             rd = run_details
             rd.last_updated_by = 0
             rd.last_update_date = now
             rd.run_status = 'Open'
             rd.save()
         else:
             rds = RunDetails.objects.filter(station_gpio_id=gpio)
             for s in rds:
                 s.last_updated_by = 0
                 s.last_update_date = now
                 s.run_status = 'Open'
                 s.save()

         time.sleep(seconds)
         GPIO.setmode(GPIO.BCM)
         GPIO.setup(gpio, GPIO.OUT)
         GPIO.output(gpio, GPIO.LOW)  # Close valve
         print("Closed Station:", station, 'GPIO: ', gpio)

         if (ReticEngine.MASTER_STATION_GPIO != 0):
            print("Closing Master Station GPIO: ", ReticEngine.MASTER_STATION_GPIO)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(ReticEngine.MASTER_STATION_GPIO, GPIO.OUT)
            GPIO.output(ReticEngine.MASTER_STATION_GPIO, GPIO.LOW)  # Close valve

         if run_details:
             rd2 = rd
             rd2.last_updated_by = 0
             rd2.last_update_date = now
             rd2.run_status = 'Closed'
             rd2.save()
         else:
             rds = RunDetails.objects.filter(station_gpio_id=gpio)
             for s in rds:
                 s.last_updated_by = 0
                 s.last_update_date = now
                 s.run_status = 'Closed'
                 s.save()

    @staticmethod
    def closeValvesDB():

        pst = pytz.timezone('Australia/Perth')
        now = datetime.now(pst)

        GPIO.setmode(GPIO.BCM)

        # loop over the LEDs on the TrafficHat and light each one
        # individually
        if (ReticEngine.MASTER_STATION_GPIO != 0):
            GPIO.setup(ReticEngine.MASTER_STATION_GPIO, GPIO.OUT)
            print("Closing Master Station GPIO: ", ReticEngine.MASTER_STATION_GPIO)
            GPIO.output(ReticEngine.MASTER_STATION_GPIO, GPIO.LOW)  # Close valve

        for i in ReticEngine.get_stations():
            GPIO.setup(i.station_gpio, GPIO.OUT)
            print("Close valve: " + str(i) + " | " + str(i.station_gpio))
            time.sleep(0.1)
            GPIO.output(i.station_gpio, GPIO.BOARD)

        if (ReticEngine.MASTER_STATION_GPIO != 0):
            print("Closing Master Station GPIO: ", ReticEngine.MASTER_STATION_GPIO)
            GPIO.output(ReticEngine.MASTER_STATION_GPIO, GPIO.LOW)  # Close valve

        # perform a bit of cleanup
        GPIO.cleanup()

        rds = RunDetails.objects.all()
        for s in rds:
            s.last_updated_by = 0
            s.last_update_date = now
            s.run_status = 'Closed'
            s.save()

    @staticmethod
    def item_generator(json_input, lookup_key):
        if isinstance(json_input, dict):
            for k, v in json_input.items():
                if k == lookup_key:
                    yield v
                else:
                    yield from ReticEngine.item_generator(v, lookup_key)
        elif isinstance(json_input, list):
            for item in json_input:
                yield from ReticEngine.item_generator(item, lookup_key)



    @staticmethod
    @start_new_thread
    def refreshWeather():
        s = Settings.objects.filter(id=1).first()

        #url = "http://reg.bom.gov.au/fwo/IDW60901/IDW60901.94608.json"
        url = s.bom_url

        r = requests.get(url)

        data = json.loads(r.text)

        pst = pytz.timezone('Australia/Perth')
        now = datetime.now(pst)

        Weather.objects.all().delete()

        #for i in range(len(data['observations']['data'])):
        for i in range(0,10):
            w = Weather()
            for key, value in data['observations']['data'][i].items():
                #print(key,value)
                if (key == 'sort_order'):
                    w.sort_order = value
                elif (key == 'name'):
                    w.name = value
                elif (key == 'local_date_time_full'):
                    w.local_date_time_full = value
                elif (key == 'apparent_t'):
                    w.apparent_t = value
                elif (key == 'delta_t'):
                    w.delta_t = value
                elif (key == 'gust_kmh'):
                    w.gust_kmh = value
                elif (key == 'air_temp'):
                    w.air_temp = value
                elif (key == 'press'):
                    w.press = value
                elif (key == 'rain_trace'):
                    w.rain_trace = value
                elif (key == 'rel_hum'):
                    w.rel_hum
                elif (key == 'wind_spd_kmh'):
                    w.wind_spd_kmh = value
                elif (key == 'wind_dir'):
                    w.wind_dir = value

                w.created_by = 0
                w.creation_date = now
                w.last_updated_by = 0
                w.last_update_date = now
                w.save()

    @staticmethod
    @start_new_thread
    def testWeather():

        if Settings.objects.filter(rain_detection=0):
            print("Rain detection not set - returning...")
            return

        weather = Weather.objects.filter(sort_order=0)
        settings = Settings.objects.all().first()

        pst = pytz.timezone('Australia/Perth')
        now = datetime.now(pst)


        for w in weather:
            print(w.rain_trace,settings.rain_threshold)
            if w.rain_trace >= settings.rain_threshold:
                print("Rain trace found..")
                for i in RunDay.objects.all().select_related('run').filter(run__status=1):
                    print("updating status..")
                    rh = RunHeaders.objects.get(id=i.run.id)
                    rh.status = 2
                    rh.last_updated_by = 0
                    rh.last_update_date = now
                    rh.save()
            elif w.rain_trace < settings.rain_threshold:
                for i in RunDay.objects.all().select_related('run').filter(run__status=2):
                    print("updating status..")
                    rh = RunHeaders.objects.get(id=i.run.id)
                    rh.status = 1
                    rh.last_updated_by = 0
                    rh.last_update_date = now
                    rh.save()



    @staticmethod
    def testRunDate():

        pst = pytz.timezone('Australia/Perth')
        now = datetime.now(pst)
        if platform == "linux" or platform == "linux2":
            print(now.strftime('%Y-%m-%d %-H:%M'))
        else:
            print(now.strftime('%Y-%m-%d %#H:%M'))

        print(now.strftime('%A'))
        today_dayofweek = now.strftime('%A')
        for i in RunDay.objects.all().select_related('run').filter(run__status=1):
            start_date = i.run.start_date.strftime('%Y-%m-%d')
            print('xx: ' + start_date)
            if now > i.run.start_date and now < i.run.end_date:
                print("start dates can run!!!")
                print(i.run.run_name + " | " + i.weekday)
                if i.weekday == today_dayofweek:
                    print("weekday can run!!")
                    print(now.strftime('%H%M') + " | " + str(i.start_time))
                    if platform == "linux" or platform == "linux2":
                        nowtime = now.strftime('%-H%M')
                    else:
                        nowtime = now.strftime('%#H%M')

                    if nowtime == str(i.start_time):
                       print("time can run!!",nowtime,i.start_time)
                       rd = i
                       rd.last_updated_by = 0
                       rd.last_update_date = now
                       rd.run_status = 'Running'
                       rd.save()

                       rh = RunHeaders.objects.get(id=i.run.id)
                       rh.last_run = now
                       rh.last_updated_by = 0
                       rh.last_update_date = now
                       rh.save()

                       print('running save')

                       print(i.run_id)
                       run_details = RunDetails.objects.filter(run_id=i.run_id)
                       for i in run_details:
                           print(i.run_id,i.station_id,i,i.station_gpio_id,i.station_seconds)

                       ReticEngine.runCycleFromDB(run_details,rd.id)
                       GPIO.cleanup()

                       rd2 = rd
                       rd2.last_updated_by = 0
                       rd2.last_update_date = now
                       rd2.run_status = ''
                       rd2.save()
                       print('finished save')

    @staticmethod
    def convert_seconds(seconds):
        import time
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

if __name__ == '__main__':
    try:
        #ReticEngine.runAllFromDB(10)
        #ReticEngine.closeValvesDB()
        #ReticEngine.refreshWeather()

        ReticEngine.testWeather()

        if len(sys.argv) > 1:
            if ( sys.argv[1] != None and sys.argv[1] == 'start' and len(sys.argv)-1 == 3):
                ReticEngine.runOneDB(sys.argv[2],int(sys.argv[3]))
            elif ( sys.argv[1] != None and sys.argv[1] == 'stop' and len(sys.argv)-1 == 2):
                ReticEngine.stopOneDB(sys.argv[2])
        else:
            ## Run the engine first
            ReticEngine.testRunDate()
            ## Now check to refresh weather
            pst = pytz.timezone('Australia/Perth')
            now = datetime.now(pst)
            if platform == "linux" or platform == "linux2":
                nowtime = now.strftime('%-H%M')
            else:
                nowtime = now.strftime('%#H%M')

            if (int(nowtime) % 20 == 0 and not int(nowtime) % 100 == 0):
                print("Running weather....")
                ReticEngine.refreshWeather()

    except:
        # Shut all valves...
        ReticEngine.closeValvesDB()
        print("An Error occured OR user stopped routine...!!!")
        raise

