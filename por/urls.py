import django_registration.forms
from django.conf.urls import url,include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import MyRegistrationFormUniqueEmail
from .views import HomeView,RegistrationViewUniqueEmail,ProfileView,ManualView,EditRunView,EditDayView,EditDetailsView,EditStationView,StationView,SettingsView,DoorStatusView,MyPasswordResetView
from .routers import router
from django.contrib.auth.models import User, Group

admin.autodiscover()

""""
  Custom hook for new fields
"""
def user_created(sender, user, request, **kwargs):
    """
    Called via signals when user registers. Creates different profiles and
    associations
    """
    form = MyRegistrationFormUniqueEmail(request.POST)
    # Update first and last name for user
    user.first_name=form.data['first_name']
    user.last_name=form.data['last_name']
    user.save()

from django_registration.signals import user_registered
user_registered.connect(user_created)

from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

from django.conf import settings
myappname = settings.MYAPPNAME
myappname_slash = '/' + settings.MYAPPNAME

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^' + myappname +  '/home/$', HomeView.as_view(success_url=myappname_slash + "/home/"), name='home'),
    url(r'^' + myappname +  '/login/$', auth_views.LoginView, {'template_name': myappname + '/login.html'}, name='login'),
    url(r'^' + myappname +  '/logout/$', auth_views.LogoutView, {'next_page': 'login'}, name='logout'),
    url(r'^' + myappname +  '/profile/', ProfileView.as_view(success_url=myappname + "/profile/"), name='profile'),
    url(r'^' + myappname +  '/accounts/register/$',  RegistrationViewUniqueEmail.as_view(),name='register'),
    url(r'^' + myappname +  '/manual/',  ManualView.as_view(),name='manual_view'),
    url(r'^' + myappname +  '/editrun/$',  EditRunView.as_view(),name='editrun_view'),
    url(r'^' + myappname +  '/editday/$',  EditDayView.as_view(),name='editday_view'),
    url(r'^' + myappname +  '/addday/$',  EditDayView.as_view(),name='addday_view'),
    url(r'^' + myappname +  '/addcycle/$',  EditRunView.as_view(),name='addcycle_view'),
    url(r'^' + myappname +  '/addstation/$',  EditDetailsView.as_view(),name='addstation_view'),
    url(r'^' + myappname +  '/editdetails/$',  EditDetailsView.as_view(),name='editdetails_view'),
    url(r'^' + myappname +  '/stations/$', StationView.as_view(), name='station_view'),
    url(r'^' + myappname +  '/editstation/$',  EditStationView.as_view(),name='editstation_view'),
    url(r'^' + myappname +  '/settings/$', SettingsView.as_view(), name='settings_view'),
    url(r'^' + myappname +  '/accounts/register/$',  RegistrationViewUniqueEmail.as_view(),name='registration_register'),
    url(r'^' + myappname +  '/accounts/password/reset/$', MyPasswordResetView.as_view(), name='auth_password_reset'),
    url(r'^' + myappname +  '/accounts/reset/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'), # must be named for reverse to work
  
    url(r'^' + myappname +  '/accounts/',  include('django_registration.backends.activation.urls')),
    url(r'^' + myappname +  '/accounts/', include('django.contrib.auth.urls')),
    
    path(myappname +  '/api/', include(router.urls)),
    path(myappname + '/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)