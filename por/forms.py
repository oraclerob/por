import django.contrib.auth.forms
from django import forms
from django_registration.forms import RegistrationFormUniqueEmail, User
from .models import Stations,RunHeaders,RunDetails,RunDay,Settings



class MyRegistrationFormUniqueEmail(RegistrationFormUniqueEmail):

    first_name = forms.CharField(widget=forms.TextInput(),error_messages={'required': 'First name is required'})
    last_name = forms.CharField(widget=forms.TextInput(), error_messages={'required': 'Last name is required'})
    password1 = forms.CharField(widget=forms.PasswordInput() ,error_messages={'required': 'Password is required'})
    password2 = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': 'Password is required'})

    def __init__(self, *args, **kwargs):
        super(MyRegistrationFormUniqueEmail, self).__init__(*args, **kwargs)


class HomeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)

class ActivateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ActivateForm, self).__init__(*args, **kwargs)

class ManualForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ManualForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['station_number']
        model = Stations

class EditRunForm(forms.ModelForm):

    start_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    end_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )

    def __init__(self, *args, **kwargs):
        super(EditRunForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['run_name','status','start_date','end_date']
        model = RunHeaders
        

class EditDayForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(EditDayForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['weekday','start_time']
        model = RunDay

class EditDetailsForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(EditDetailsForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['station','station_seconds']
        model = RunDetails

class EditStationForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(EditStationForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['status','station_default_seconds']
        model = Stations


class SettingsForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['rain_detection', 'bom_url', 'rain_threshold']
        model = Settings

# class AddVenueForm(forms.ModelForm):
#
#     #object_name       = forms.CharField(widget=forms.TextInput(),disabled=True)
#     #formatted_address = forms.CharField(widget=forms.TextInput(), error_messages={'required': '*'})
#     #google_maps_url   = forms.CharField(widget=forms.TextInput(), error_messages={'required': '*'})
#     #lattitude         = forms.CharField(widget=forms.TextInput(), error_messages={'required': '*'})
#     #longitude         = forms.CharField(widget=forms.TextInput(), error_messages={'required': '*'})
#     #website_url       = forms.CharField(widget=forms.TextInput(), error_messages={'required': '*'})
#
#     class Meta:
#         model = Venues
#         fields = ['venue_name', 'formatted_address', 'google_maps_url', 'lattitude','longitude','website_url','place_id']
#
#     def __init__(self, *args, **kwargs):
#         super(AddVenueForm, self).__init__(*args, **kwargs)
#         #self.fields['object_name'].widget.attrs['readonly'] = True
#         #self.fields['formatted_address'].disabled = True
#         #self.fields['google_maps_url'].disabled = True
#         #self.fields['lattitude'].disabled = True
#         #self.fields['longitude'].disabled = True
#         #self.fields['website_url'].disabled = True
#
# class AddDrinksForm(forms.ModelForm):
#
#     class Meta:
#         model = Drinks
#         fields = ['drink_name', 'price', 'drink_size','hh_price','hh_days','hh_time_start','hh_time_end']
#
#     def __init__(self, *args, **kwargs):
#         super(AddDrinksForm, self).__init__(*args, **kwargs)
#
# class EditDrinksForm(forms.ModelForm):
#
#     class Meta:
#         model = Drinks
#         fields = ['drink_name', 'price', 'drink_size','hh_price','hh_days','hh_time_start','hh_time_end']
#
#     def __init__(self, *args, **kwargs):
#         super(EditDrinksForm, self).__init__(*args, **kwargs)
#
# class DrinksForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super(DrinksForm, self).__init__(*args, **kwargs)

class UserProfileForm(forms.ModelForm):

    password1 = forms.CharField(max_length=128,required=False)
    password2 = forms.CharField(max_length=128,required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['first_name', 'last_name']
        model = User






