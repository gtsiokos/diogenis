from django.conf.urls.defaults import *

from diogenis.teachers.views import *


urlpatterns = patterns('',
    url(r'^(?P<username>\w{0,50})/$', manage_labs, name='teachers.index'),
    url(r'^(?P<username>\w{0,50})/pending-students/$', manage_labs, name='teachers.pending-students'),
    url(r'^delete-lab/(?P<username>\w{0,50})/(?P<hash_id>[a-zA-Z0-9]{0,64})/$', delete_lab, name='teachers.delete-lab'),
    url(r'^submit-student-to-lab/$', submit_student_to_lab),
    url(r'^add-new-lab/$', add_new_lab),
    url(r'^delete-subscription/$', delete_subscription),
    url(r'^update-absences/$', update_absences),
    url(r'^export-pdf/(?P<hash_id>[a-zA-Z0-9]{0,64})/$', export_pdf),
)
