from django.conf.urls.defaults import *

from diogenis.students.views import *


urlpatterns = patterns('',
    url(r'^(?P<username>\w{0,50})/$', display_labs, name='students.index'),
    url(r'^add-new-lab/$', add_new_lab),
)
