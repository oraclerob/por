from django.contrib.sites.models import Site

def mydomain(request):
    current_site = Site.objects.get_current()
    myappname = 'por'
    myapphome = '/por/home/'
    myapploginurl = '/por/login/'
    myscheme = 'http'
    myport = str(8888)
    if myscheme == 'https':
        myport = ''

    return {
       'myappname': myappname,
       'myapphome': myapphome,
       'myapploginurl': myapploginurl,
       'mydomain': current_site.domain,
       'myport': ':' + myport,
       'myscheme': myscheme,
    }