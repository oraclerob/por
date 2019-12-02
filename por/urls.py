import registration.forms
from django.conf.urls import url,include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import MyRegistrationFormUniqueEmail
from .views import HomeView,RegistrationViewUniqueEmail,ProfileView,ManualView,EditRunView,EditDayView,EditDetailsView,EditStationView,StationView,SettingsView
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

from registration.signals import user_registered
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


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^por/home/$', HomeView.as_view(success_url="/por/home/"), name='home'),
    url(r'^por/login/$', auth_views.LoginView, {'template_name': 'por/login.html'}, name='login'),
    url(r'^por/logout/$', auth_views.LogoutView, {'next_page': 'login'}, name='logout'),
    url(r'^por/profile/', ProfileView.as_view(success_url="/por/profile/"), name='profile'),
    url(r'^por/accounts/register/$',  RegistrationViewUniqueEmail.as_view(),name='register'),
    url(r'^por/manual/',  ManualView.as_view(),name='manual_view'),
    url(r'^por/editrun/$',  EditRunView.as_view(),name='editrun_view'),
    url(r'^por/editday/$',  EditDayView.as_view(),name='editday_view'),
    url(r'^por/addday/$',  EditDayView.as_view(),name='addday_view'),
    url(r'^por/addcycle/$',  EditRunView.as_view(),name='addcycle_view'),
    url(r'^por/addstation/$',  EditDetailsView.as_view(),name='addstation_view'),
    url(r'^por/editdetails/$',  EditDetailsView.as_view(),name='editdetails_view'),
    url(r'^por/stations/$', StationView.as_view(), name='station_view'),
    url(r'^por/editstation/$',  EditStationView.as_view(),name='editstation_view'),
    url(r'^por/settings/$', SettingsView.as_view(), name='settings_view'),
    #url(r'^accounts/password/reset/confirm/[.*]/set-password/', auth_views.password_reset, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'), # must be named for reverse
    url(r'^por/accounts/password/reset/confirm/[^ ]*/set-password/auth_password_reset_complete', auth_views.PasswordResetCompleteView, {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'), # must be named for reverse to work
    url(r'^por/accounts/password/reset/auth_password_reset_done', auth_views.PasswordResetDoneView, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'), # must be named for reverse to work
    url(r'^por/accounts/', include('registration.backends.hmac.urls')),
    url(r'^por/notifications/', include('notify.urls', 'notifications')),
    path('por/api/', include(router.urls)),
    path('por/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)