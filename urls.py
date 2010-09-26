from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from diogenis.views import *
from diogenis.labs.views import *
from diogenis.students.views import *

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^admin/', include(admin.site.urls)),
    
    (r'^labs/', include('diogenis.labs.urls')),
    (r'^teachers/', include('diogenis.teachers.urls')),
    (r'^students/', include('diogenis.students.urls')),
    (r'^login/', login),
    (r'^logout/', logout),
    
    (r'^manage_db/', manage_db),
    (r'^save_db_xls/', save_db),
    (r'^save_db_labs/', fill_labs),
    (r'^api/', excel_api),
    (r'^$', index),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
