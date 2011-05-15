from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from diogenis.views import index
from diogenis.accounts.views import login, logout, signup

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^admin/', include(admin.site.urls)),
    
    (r'^labs/', include('diogenis.labs.urls')),
    (r'^teachers/', include('diogenis.teachers.urls')),
    (r'^students/', include('diogenis.students.urls')),
    (r'^system/', include('diogenis.labs.urls')),
    (r'^signup/', signup),
    (r'^login/$', login),
    (r'^logout/$', logout),
    (r'^$', index),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
