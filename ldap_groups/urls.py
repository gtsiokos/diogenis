# -*- coding: utf-8 -*-

from diogenis.ldap_groups.views import ldap_search
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^ldap_search/$', ldap_search, name='ldap_search'),
)
