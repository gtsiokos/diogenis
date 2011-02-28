# -*- coding: utf-8 -*-
try:
	from diogenis.ldap_groups.models import LDAPGroup
	from diogenis.ldap_groups.views import ldap_search
	from django.conf.urls.defaults import *
	from django.contrib import admin

	class LDAPGroupAdmin(admin.ModelAdmin):
		class Media:
		    js = ("js/jquery-1.3.2.min.js",
		          "js/jquery.livequery.js",
		        )
		def get_urls(self):
		    urls = super(LDAPGroupAdmin, self).get_urls()
		    my_urls = patterns('',
		        (r'^ldap_search/$', self.admin_site.admin_view(ldap_search)),
		    )
		    
		    return my_urls + urls

	admin.site.register(LDAPGroup, LDAPGroupAdmin)
except:
	pass
