from django.conf.urls.defaults import *

from diogenis.teachers.views import *


urlpatterns = patterns('',
	(r'^(?P<username>\w{0,50})/$', manage_labs),
	(r'^(?P<username>\w{0,50})/pending-students/$', manage_labs),
	(r'^submit-student-to-lab/$', submit_student_to_lab),
	(r'^add-new-lab/$', add_new_lab),
	(r'^export-pdf/(?P<name>\w{0,20})/(?P<day>\w{0,20})/(?P<start_hour>\d+)/(?P<end_hour>\d+)/(?P<csrf_token>[a-zA-Z0-9]{0,64})/$', export_pdf),
)
