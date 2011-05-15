from django.conf.urls.defaults import *

from diogenis.students.views import *


urlpatterns = patterns('',
    (r'^(?P<username>\w{0,50})/$', display_labs),
    (r'^add-new-lab/$', add_new_lab),
)
