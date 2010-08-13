from django.conf.urls.defaults import *

from diogenis.teachers.views import *


urlpatterns = patterns('',
	(r'^(?P<username>\w{0,50})/', labs),
)
