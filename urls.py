from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.http import HttpResponse

from diogenis.views import index
from diogenis.auth.views import login, logout, signup

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^teachers/', include('diogenis.teachers.urls')),
    url(r'^students/', include('diogenis.students.urls')),
    url(r'^schools/', include('diogenis.schools.urls')),
    url(r'^signup/', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$', index, name='index'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if hasattr(settings,'BLITZ_ACCOUNTS'):
    def verify_blitz(request):
        return HttpResponse('42')
        
    def make_url(blitz_account):
        blitz_url = r'^%s/$' % blitz_account
        return url(blitz_url, verify_blitz)

    blitz_urlpatterns = map(make_url, settings.BLITZ_ACCOUNTS)
    urlpatterns += blitz_urlpatterns

