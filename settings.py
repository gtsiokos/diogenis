# Django settings for diogenis project.

import os.path
from local_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MANAGERS = ADMINS

DATABASE_ENGINE = 'django.db.backends.sqlite3'           									# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'diogenis.db')		# Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8080/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n$3ho=zlga1q5vjh83^_ji%flfqj)q#3%r1u90r_)j0#b@6%-%'

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
# MY ADDITIONS FOR LDAP 
    'diogenis.ldap_groups',# 'diogenis.LDAPGroup', 'diogenis.LDAPGroupAdmin',
)

AUTHENTICATION_BACKENDS = (
	'diogenis.ldap_groups.accounts.backends.ActiveDirectoryGroupMembershipSSLBackend',
	'django.contrib.auth.backends.ModelBackend',
)

# Needed for the decorator
LOGIN_URL = '/'

# Needed for the custom user profile
								##			WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! 
								##			WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! 
								##			WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! 
								##			WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! 
								##			WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! WARNING!!! 
								## UPARXEI H IDIA METAVLHTH STHN ARXH TOU ARXEIOU ME TIMH TO PATH TOU PALIOY APP 'accounts' TOU DIOGENH.
#AUTH_PROFILE_MODULE = 'user.LdapProfile'

# LDAP
LDAP_SERVER = 'localhost'
LDAP_PORT = 389
LDAP_URL = 'ldap://%s:%s' % (LDAP_SERVER, LDAP_PORT)
SEARCH_DN = 'ou=teilarStudents,dc=teilar,dc=gr'
SEARCH_FIELDS = ['*']
