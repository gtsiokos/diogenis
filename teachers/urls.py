from django.conf.urls.defaults import *

from diogenis.teachers.views import *


urlpatterns = patterns('',
	(r'^(?P<username>\w{0,50})/', manage_labs),
	(r'^(?P<username>\w{0,50})/pending-students/', manage_labs),
	(r'^(?P<hashed_request>[a-zA-Z0-9]{0,64})/submit-student-to-lab/', submit_student_to_lab),
	(r'^(?P<hashed_request>[a-zA-Z0-9]{0,64})/add-new-lab/', add_new_lab),
	(r'^(?P<hashed_request>[a-zA-Z0-9]{0,64})/export-pdf/', export_pdf),
)
