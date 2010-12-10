from django.conf.urls.defaults import *

from diogenis.labs.views import *


urlpatterns = patterns('',
(r'^admin/$', control_panel),
)
