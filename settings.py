# -*- coding: utf-8 -*-
# Django settings for diogenis project.

import os.path

try:
	from diogenis.local_settings import *
except:
	pass

DEBUG = True
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Athens'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'diogenis.urls'

TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'diogenis.accounts', 'diogenis.labs',
    'diogenis.teachers', 'diogenis.students',
	'diogenis.ldap_groups',# 'diogenis.LDAPGroup', 'diogenis.LDAPGroupAdmin',
	'south',
)

try:
	import ldap
	AUTHENTICATION_BACKENDS = (
		'diogenis.ldap_groups.accounts.backends.ActiveDirectoryGroupMembershipSSLBackend',
		'django.contrib.auth.backends.ModelBackend',
	)
except:
	pass	

# Needed for the decorator
LOGIN_URL = '/'

# LDAP
LDAP_SERVER = 'localhost'
LDAP_PORT = 389
LDAP_URL = 'ldap://%s:%s' % (LDAP_SERVER, LDAP_PORT)
SEARCH_DN = 'ou=teilarStudents,dc=teilar,dc=gr'
SEARCH_FIELDS = ['*']
