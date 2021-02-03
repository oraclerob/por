import threading
from _datetime import datetime

#import selenium.webdriver.firefox.firefox_binary
import django.http
import django_registration.forms
import requests
from django.utils import timezone
import pytz
from django.views.generic import FormView,RedirectView,UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db.models import Sum,Count
from django_tables2 import RequestConfig
from django.db.models import Q
from django.db import IntegrityError
from django.utils.dateformat import DateFormat
from django.http import JsonResponse

from django_registration.backends.activation.views import RegistrationView
from .retic_engine import ReticEngine
from .forms import ManualForm,EditRunForm,EditDayForm,EditDetailsForm,EditStationForm,SettingsForm


from .forms import HomeForm,UserProfileForm,MyRegistrationFormUniqueEmail
# from .forms import HomeForm, AddVenueForm, AddDrinksForm, DrinksForm, EditDrinksForm, UserProfileForm
# from .forms import MyRegistrationFormUniqueEmail
from .tables import StationTable, StationGPIOMappingsTable, RunHeaderTable, RunDetailsTable, RunDayTable,WeatherTable

from .models import Stations,Station_GPIO_Mappings,RunDetails,RunDay,RunHeaders,Weather,Settings

from django.conf import settings
myappname = settings.MYAPPNAME
myappname_slash = '/' + settings.MYAPPNAME

def menu_list(self,list):
     ## Garage door
    pst = pytz.timezone('Australia/Perth')
    now = datetime.now(pst)
    try: 
        gd_last = GarageDoor.objects.latest('creation_date')
    except:
        gd_last = GarageDoor()
    import RPi.GPIO as gpio
    gpio.setmode(gpio.BCM)
    gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
    if gpio.input(16) == 0:
        gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
        diff = (now - gd_last.creation_date.astimezone(pst)).total_seconds()
        self.request.session['garage_door_state'] = 'Closed'
        self.request.session['garage_door'] = 'Closed ' + ReticEngine.convert_seconds(diff)
        self.request.session['garage_door_time'] = ReticEngine.convert_seconds(diff)
    else:
        gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        diff = (now - gd_last.creation_date.astimezone(pst)).total_seconds()
        self.request.session['garage_door_state'] = 'Open'
        self.request.session['garage_door'] = 'Open ' + ReticEngine.convert_seconds(diff)
        self.request.session['garage_door_time'] = ReticEngine.convert_seconds(diff)

    if (list == 'list11'):
        self.request.session['menu1_active'] = 'active';
        self.request.session['menu1_collapse'] = '';
        self.request.session['menu1_collapsed'] = '';
        self.request.session['menu2_active'] = '';
        self.request.session['menu2_collapse'] = 'collapse';
        self.request.session['menu2_collapsed'] = 'collapsed';
        self.request.session['menu3_active'] = '';
        self.request.session['menu3_collapse'] = 'collapse';
        self.request.session['menu3_collapsed'] = 'collapsed';
        self.request.session['menu4_active'] = '';
        self.request.session['menu4_collapse'] = 'collapse';
        self.request.session['menu4_collapsed'] = 'collapsed';
        self.request.session['list11_active'] = 'active';
        self.request.session['list21_active'] = ''
        self.request.session['list22_active'] = ''
        self.request.session['list31_active'] = ''
        self.request.session['list41_active'] = ''
    elif (list == 'list21'):
        self.request.session['menu1_active'] = '';
        self.request.session['menu1_collapse'] = '';
        self.request.session['menu1_collapsed'] = '';
        self.request.session['menu2_active'] = 'active';
        self.request.session['menu2_collapse'] = '';
        self.request.session['menu2_collapsed'] = '';
        self.request.session['menu3_active'] = '';
        self.request.session['menu3_collapse'] = 'collapse';
        self.request.session['menu3_collapsed'] = 'collapsed';
        self.request.session['menu4_active'] = '';
        self.request.session['menu4_collapse'] = 'collapse';
        self.request.session['menu4_collapsed'] = 'collapsed';
        self.request.session['list11_active'] = '';
        self.request.session['list21_active'] = 'active'
        self.request.session['list22_active'] = ''
        self.request.session['list31_active'] = ''
        self.request.session['list41_active'] = ''
    elif (list == 'list22'):
        self.request.session['menu1_active'] = '';
        self.request.session['menu1_collapse'] = 'collapse';
        self.request.session['menu1_collapsed'] = 'collapsed';
        self.request.session['menu2_active'] = 'active';
        self.request.session['menu2_collapse'] = '';
        self.request.session['menu2_collapsed'] = '';
        self.request.session['menu3_active'] = '';
        self.request.session['menu3_collapse'] = 'collapse';
        self.request.session['menu3_collapsed'] = 'collapsed';
        self.request.session['menu4_active'] = '';
        self.request.session['menu4_collapse'] = 'collapse';
        self.request.session['menu4_collapsed'] = 'collapsed';
        self.request.session['list11_active'] = '';
        self.request.session['list21_active'] = ''
        self.request.session['list22_active'] = 'active'
        self.request.session['list31_active'] = ''
        self.request.session['list41_active'] = ''

    elif (list == 'list31'):
        self.request.session['menu1_active'] = '';
        self.request.session['menu1_collapse'] = 'collapse';
        self.request.session['menu1_collapsed'] = 'collapsed';
        self.request.session['menu2_active'] = '';
        self.request.session['menu2_collapse'] = 'collapse';
        self.request.session['menu2_collapsed'] = 'collapsed';
        self.request.session['menu3_active'] = 'active';
        self.request.session['menu3_collapse'] = 'collapse';
        self.request.session['menu3_collapsed'] = 'collapsed';
        self.request.session['menu4_active'] = '';
        self.request.session['menu4_collapse'] = 'collapse';
        self.request.session['menu4_collapsed'] = 'collapsed';
        self.request.session['list11_active'] = '';
        self.request.session['list21_active'] = ''
        self.request.session['list22_active'] = ''
        self.request.session['list31_active'] = 'active'
        self.request.session['list41_active'] = ''
    elif (list == 'list41'):
        self.request.session['menu1_active'] = '';
        self.request.session['menu1_collapse'] = 'collapse';
        self.request.session['menu1_collapsed'] = 'collapsed';
        self.request.session['menu2_active'] = '';
        self.request.session['menu2_collapse'] = 'collapse';
        self.request.session['menu2_collapsed'] = 'collapsed';
        self.request.session['menu3_active'] = '';
        self.request.session['menu3_collapse'] = 'collapse';
        self.request.session['menu3_collapsed'] = 'collapsed';
        self.request.session['menu4_active'] = 'active';
        self.request.session['menu4_collapse'] = 'collapse';
        self.request.session['menu4_collapsed'] = 'collapsed';
        self.request.session['list11_active'] = '';
        self.request.session['list21_active'] = ''
        self.request.session['list22_active'] = ''
        self.request.session['list31_active'] = ''
        self.request.session['list41_active'] = 'active'

def init_session(self,request):
    None


class HomeView(FormView):

    template_name = 'por/home.html'
    form_class = HomeForm

    def get(self,request):

        menu_list(self,'list11')
        vote_count = 0

        init_session(self,request)

        if request.GET.get('stoprun') == 'Y':
            ReticEngine.stopRun(request.GET.get('stop_run_id'))


        #table = StationTable(Stations.objects.filter(Q(venue_id=request.GET.get('venue_id'))))
        headertable = RunHeaderTable(RunHeaders.objects.all())        # get the queryset
        if request.GET.get('run_id'):
            qheadertable = RunHeaders.objects.filter(id=request.GET.get('run_id')).get() # Get the first object
            rchecked = 'r' + request.GET.get('run_id')
        else:
            qheadertable = RunHeaders.objects.all()[:1].get() # Get the first object
            rchecked = 'r1'

        #detailtable = RunDetailsTable(RunDetails.objects.filter(Q(run_id=request.GET.get('run_id'))))
        detailtable = RunDetailsTable(RunDetails.objects.filter(run_id=qheadertable.id))
        rundaytable = RunDayTable(RunDay.objects.filter(run_id=qheadertable.id))

        weathertable = WeatherTable(Weather.objects.order_by('sort_order').filter(Q(sort_order=0) | Q(sort_order=1) | Q(sort_order=2)  | Q(sort_order=3)))
        weather = Weather.objects.order_by('sort_order').filter(Q(sort_order=0)).first()

        return render(request, 'por/home.html',{'weathertable': weathertable
                                                ,'weather': weather
                                                ,'rchecked': rchecked
                                                ,'run_name': qheadertable.run_name
                                                ,'headertable' : headertable
                                                ,'detailtable' : detailtable
                                                ,'rundaytable' : rundaytable
                                                ,'run_id' : request.GET.get('run_id')})


    def post(self, request):
        vote_count = 0

        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)
            if key == 'up' and request.POST[key] == 'true':
                vote_count = 1
            elif key == 'down' and request.POST[key] == 'true':
                vote_count = -1

        rd = RunDay.objects.filter(id=request.POST.get('runday_id'))

        if request.POST.get('stop') == 'true':
            pst = pytz.timezone('Australia/Perth')
            now = datetime.now(pst)
            for s in rd:
                s.last_updated_by = 0
                s.last_update_date = now
                s.run_status = 'Stopped'
                s.save()


        return render(request, 'por/home.html',{'runday':rd})

class ManualView(FormView):

    template_name = 'por/manual.html'
    form_class = ManualForm

    def get(self,request):

        menu_list(self,'list21')
        vote_count = 0

        init_session(self,request)

        #table = StationTable(Stations.objects.filter(Q(venue_id=request.GET.get('venue_id'))))
        station_table = Stations.objects.filter(~Q(station_number='Master'))

        return render(request, 'por/manual.html',{'station_table' : station_table,})


    def post(self, request):
        vote_count = 0

        menu_list(self, 'list21')

        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)

        user_form = Stations.objects.filter(Q(id=request.user.id)).first()
        form = ManualForm(request.POST, instance=user_form)
        station_table = Stations.objects.filter(~Q(station_number='Master'))



        station_number = self.request.POST.get('station_number')

        #if form.is_valid():
        if self.request.POST.get('btn_start'):
            ReticEngine.runOneDB(self.request.POST.get('station_number'),int(self.request.POST.get('seconds')))
        elif self.request.POST.get('btn_stop'):
            ReticEngine.closeValvesDB()
        elif self.request.POST.get('btn_systest'):
            ReticEngine.runAllFromDB(int(self.request.POST.get('sysseconds')))
        elif self.request.POST.get('btn_sysstop'):
            ReticEngine.closeValvesDB()

            #user_form = form.save(commit=False)
            #user_form.save()
        #else:
        #    print("form invalid!!")
        #    return render(request, 'por/manual.html', {'form': form})

        return render(request, myappname + '/manual.html', {'station_table': station_table, 'station_number': station_number,})

class EditRunView(FormView):

    template_name = 'por/editrun.html'
    form_class = EditRunForm

    def get(self,request):

        menu_list(self,'list31')
        vote_count = 0

        init_session(self,request)

        form = RunHeaders.objects.filter(Q(id=self.request.GET.get('run_id'))).first()

        if request.GET.get('run_id') is None:
             form = RunHeaders()
             form.id = ''

        pst = pytz.timezone('Australia/Perth')
        form.start_date = form.start_date.astimezone(pst)
        form.end_date = form.end_date.astimezone(pst)
       
        df = DateFormat(form.start_date) 
        form.start_date = df.format('Y-m-d')
        df = DateFormat(form.end_date) 
        form.end_date = df.format('Y-m-d')
        
        return render(request, 'por/editrun.html',{'form' : form,})

    def post(self, request):
        vote_count = 0

        menu_list(self, 'list31')

        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)

        if request.POST.get('id') == '':
            user_form = RunHeaders()
            form = EditRunForm(request.POST,instance=user_form)
            form.id = ''
        else:
            user_form = RunHeaders.objects.filter(Q(id=self.request.POST.get('run_id'))).first()
            form = EditRunForm(request.POST, instance=user_form)
            
        if form.is_valid():
            if self.request.POST.get('btn_delete'):
                print('deleting',request.POST.get('id'))
                delete_h = RunHeaders.objects.filter(Q(id=self.request.POST.get('id')))
                delete_h.delete()
                delete_d = RunDay.objects.filter(Q(id=self.request.POST.get('run_id')))
                delete_d.delete()
            else:
                user_form = form.save(commit=False)
                user_form.last_updated_by = 0
                user_form.last_update_date = datetime.now()
                user_form.save()
        else:
            print("form invalid!!", form.errors)
            return render(request, 'por/editrun.html', {'form': form})

        return django.http.HttpResponseRedirect(myappname_slash + '/home/')
        #return render(request, 'por/manual.html', {'station_table': station_table, 'station_number': station_number,})

class EditDayView(FormView):

    template_name = 'por/editday.html'
    form_class = EditDayForm

    def get(self,request):

        menu_list(self,'list32')

        init_session(self,request)

        form = ''
        start_time = '0'

        if request.GET.get('id') is not None:
            form = RunDay.objects.filter(Q(id=self.request.GET.get('id'))).first()
            import math
            hour = int(math.floor(form.start_time / 100))
            rem = int(form.start_time % 100)
            start_time = str(hour) + ':' + str(rem)
        else:
            form = RunDay()
            form.run_id = self.request.GET.get('run_id')
            form.id = ''

        return render(request, 'por/editday.html',{'form' : form,'start_time' : start_time})

    def post(self, request):

        menu_list(self, 'list32')

        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)

        if request.POST.get('id') != '':
            user_form = RunDay.objects.filter(Q(id=self.request.POST.get('id'))).first()
            form = EditDayForm(request.POST, instance=user_form)
        else:
            form = EditDayForm(request.POST)
            form.run_id = request.POST.get('run_id')
            form.start_time =  int(request.POST['xstart_time'].replace(':',''))
            

        if form.is_valid():
            if self.request.POST.get('btn_delete'):
                print('deleting',request.POST.get('id'))
                delete_form = RunDay.objects.filter(Q(id=self.request.POST.get('id')))
                delete_form.delete()
            else:
                user_form = form.save(commit=False)
                if request.POST.get('id') == '':
                    user_form.run_id = form.run_id
                user_form.start_time =  int(request.POST['xstart_time'].replace(':',''))
                user_form.last_updated_by = 0
                user_form.last_update_date = datetime.now()
                if self.request.POST.get('btn_stop'):
                    user_form.run_status = 'Stopped'
                user_form.save()
        else:
            print("form invalid!!", form.errors)
            return render(request, 'por/editday.html', {'form': form})

        return django.http.HttpResponseRedirect(myappname_slash + '/home/?run_id=' + str(request.POST.get('run_id')))
        #return render(request, 'por/manual.html', {'station_table': station_table, 'station_number': station_number,})


class EditDetailsView(FormView):

    template_name = 'por/editdetails.html'
    form_class = EditDetailsForm

    def get(self,request):

        menu_list(self,'list33')

        init_session(self,request)

        form = RunDetails.objects.filter(Q(id=self.request.GET.get('id'))).first()
        stations = Stations.objects.all()

        return render(request, 'por/editdetails.html',{'form' : form,'add_run_id' : request.GET.get('run_id'), 'stations' : stations})

    def post(self, request):

        menu_list(self, 'list32')

        for key in request.POST:
            print(key,request.POST[key])
        
        if request.POST.get('id') == '':
            form = EditDetailsForm(request.POST)  
            station_gpio = Station_GPIO_Mappings.objects.filter(Q(station_id=self.request.POST.get('station'))).first()
        else:
            user_form = RunDetails.objects.filter(Q(id=self.request.POST.get('id'))).first()
            station_gpio = Station_GPIO_Mappings.objects.filter(Q(station_id=self.request.POST.get('station'))).first()
            form = EditDetailsForm(request.POST, instance=user_form)
    
        if form.is_valid():
            if self.request.POST.get('btn_delete'):
                print('deleting',request.POST.get('id'))
                delete_form = RunDetails.objects.filter(Q(id=self.request.POST.get('id')))
                delete_form.delete()
            else:
                user_form = form.save(commit=False)
                if request.POST.get('id') == '':
                    user_form.run_id = request.POST.get('add_run_id')
                    user_form.station_id = request.POST.get('station')
                    user_form.station_gpio_id = station_gpio.station_gpio
                user_form.run_status = 'Closed'
                user_form.station_gpio_id = station_gpio.station_gpio
                user_form.last_updated_by = 0
                user_form.last_update_date = datetime.now()
                user_form.save()
        else:
            print("form invalid!!", form.errors)
            return render(request, 'por/editdetails.html', {'form': form,'stations' : stations})

        if request.POST.get('run_id') == '':
            return django.http.HttpResponseRedirect(myappname_slash + '/home/?run_id=' + str(request.POST.get('add_run_id')))
        else:
             return django.http.HttpResponseRedirect(myappname_slash + '/home/?run_id=' + str(request.POST.get('run_id')))
        #return render(request, 'por/manual.html', {'station_table': station_table, 'station_number': station_number,})

class StationView(FormView):

    template_name = myappname + '/stations.html'

    def get(self,request):

        menu_list(self,'list31')
        vote_count = 0

        init_session(self,request)


        table = StationTable(Stations.objects.all())


        return render(request, 'por/stations.html',{'table' : table})


    def post(self,request):

        menu_list(self,'list31')
        vote_count = 0

        init_session(self,request)

        for key in request.POST:
            value = request.POST[key]
            print(key,value)


        station = Stations.objects.filter(id=request.POST.get('station_checked')).first()
        if station.status == 0:
            station.status = 1
        else:
            station.status = 0

        station.last_updated_by = 0
        station.last_update_date = datetime.now()
        station.save()

        table = StationTable(Stations.objects.all())


        return render(request, 'por/stations.html',{'table' : table})


class EditStationView(FormView):

    template_name = 'por/editdetails.html'
    form_class = EditStationForm

    def get(self,request):

        menu_list(self,'list31')


        init_session(self,request)

        form = Stations.objects.filter(Q(id=self.request.GET.get('id'))).first()
        gpio = Station_GPIO_Mappings.objects.filter(station_id=request.GET.get('id')).first()

        return render(request, 'por/editstation.html',{'form' : form,'gpio' : gpio})

    def post(self, request):

        menu_list(self, 'list31')

        for key in request.POST:
            print(key,request.POST[key])

        user_form = Stations.objects.filter(Q(id=self.request.POST.get('id'))).first()
        form = EditStationForm(request.POST, instance=user_form)
        gpio = Station_GPIO_Mappings.objects.filter(station_id=request.POST.get('id')).first()
        new_gpio = Station_GPIO_Mappings.objects.filter(station_gpio=request.POST.get('gpio')).first()

        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.last_updated_by = 0
            user_form.last_update_date = datetime.now()
            user_form.save()
            ## Update the foreign keys
            #RunDetails.objects.filter(Q(station_gpio=gpio.station_gpio)).update(station_gpio=new_gpio.station_gpio)
            #Station_GPIO_Mappings.objects.filter(station_gpio=gpio.station_gpio).update(station_gpio=new_gpio.station_gpio)

           
          
        else:
            print("form invalid!!", form.errors)
            return render(request, 'por/editstation.html', {'form': form})

        return django.http.HttpResponseRedirect(myappname_slash + '/stations/')
        #return render(request, 'por/manual.html', {'station_table': station_table, 'station_number': station_number,})

@method_decorator(login_required, name='dispatch')
class ProfileView(FormView):
    template_name = 'por/profile.html'
    form_class = UserProfileForm

    def get(self,request):
        #menu_list(self, 'list22')

        init_session(self, request)

        user_form =  registration.forms.User.objects.filter(Q(id=request.user.id)).first()

        return render(request, 'por/profile.html', {'form' : user_form})

    def post(self,request):
        #menu_list(self, 'list22')

        user_form = registration.forms.User.objects.filter(Q(id=request.user.id)).first()

        form = UserProfileForm(request.POST,instance=user_form)

        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
        else:
            print("form invalid!!")
            return render(request, 'por/profile.html', {'form': form})

        return django.http.HttpResponseRedirect(myappname_slash + '/home/')

class SettingsView(FormView):

    template_name = myappname_slash + '/settings.html'
    form_class = SettingsForm

    def get(self,request):

        menu_list(self,'list41')

        init_session(self,request)

        form = Settings.objects.filter(id=1).first()

        return render(request, 'por/settings.html',{'form' : form,})

    def post(self, request):

        menu_list(self, 'list41')

        for key in request.POST:
            value = request.POST[key]
            print(key,value)

        if self.request.POST.get('btn_runbom'):
            print("Refreshing weather data")
            ReticEngine.refreshWeather()
            print("Refreshing weather data")
            return django.http.HttpResponseRedirect(myappname_slash + '/home/')

        user_form = Settings.objects.filter(Q(id=self.request.POST.get('id'))).first()
        form = SettingsForm(request.POST, instance=user_form)

        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.last_updated_by = 0
            user_form.last_update_date = datetime.now()
            user_form.save()
        else:
            print("form invalid!!", form.errors)
            return render(request, 'por/settings.html', {'form': form})

        return render(request, 'por/settings.html', {'form': user_form})

class RegistrationViewUniqueEmail(RegistrationView):
    template_name = 'registration/registration_form.html'
    form_class = MyRegistrationFormUniqueEmail

    def get(self,request):
        menu_list(self, 'list21')
        form = MyRegistrationFormUniqueEmail()
        return render(request, 'registration/registration_form.html', {'form': form})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if result['success']:
            return super(RegistrationViewUniqueEmail, self).form_valid(form)
        else:
            return super(RegistrationViewUniqueEmail, self).form_invalid(form)



class DoorStatusView(FormView):

    def get(self,request):

        data = GarageDoor.objects.values_list('status', 'creation_date').latest('creation_date')
        
        return JsonResponse(({'results': list(data)}))

from django.contrib.auth.views import PasswordResetView
class MyPasswordResetView(PasswordResetView):
    from django.contrib.auth.forms import PasswordResetForm
    from django.contrib.auth.tokens import default_token_generator

    template_name = 'django_registration/password_reset_form.html'
    # form_class = PasswordResetForm
    # token_generator = default_token_generator
    # from_email = 'rmascaro@scnet.com.au'
    # email_template_name = 'registration/password_reset_email.html'
    # subject_template_name = 'registration/password_reset_subject.txt'
    # html_email_template_name = 'registration/password_reset_email.html'
    # extra_email_context = ''

    def post(self, request, *args, **kwargs):
         #print('xxxxx' + str(request.body))
         return super(MyPasswordResetView, self).post(request, *args, **kwargs)


    def form_valid(self, form):
        from django.contrib.auth.views import PasswordResetView
        from django.urls import reverse_lazy
        

        #self.object = form.save(commit=False)
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, verify=False)
        result = r.json()
        ''' End reCAPTCHA validation '''
    
        if result['success']:
            #PasswordResetView.as_view((self.request))
            return super(MyPasswordResetView, self).form_valid(form)
        else:
            return super(MyPasswordResetView, self).form_invalid(form)