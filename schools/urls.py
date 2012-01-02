from django.conf.urls.defaults import *

from diogenis.schools.views import *

urlpatterns = patterns('',
    url(r'^(?P<username>\w{0,50})/$', index, name='schools.index'),
    url(r'^(?P<username>\w{0,50})/activate-subscriptions$', subscriptions_activation, name='schools.subscriptions_activation'),
    url(r'^(?P<username>\w{0,50})/teachers/$', teacher, name='schools.teachers'),
    url(r'^(?P<username>\w{0,50})/teachers/(?P<hash_id>\w{0,64})/$', teacher),
    url(r'^(?P<username>\w{0,50})/classrooms/$', classroom, name='schools.classrooms'),
    url(r'^(?P<username>\w{0,50})/classrooms/(?P<hash_id>\w{0,64})/$', classroom),
)
