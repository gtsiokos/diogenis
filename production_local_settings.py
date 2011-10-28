# -*- coding: utf-8 -*-
import os.path
import redis

# Change PROJECT_ROOT to reflect your own dir
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Change to True for development boxes
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Change them to reflect your own db settings
DATABASES = {
    'default': {
        'ENGINE':   'mysql',
        'NAME':     'diogenis',
        'USER':     'diogenis',
        'PASSWORD': 'diogenis',
        'HOST':     '',
        'PORT':     ''
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT+'/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT+'/common/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# used to send mails by sendmail
EMAIL_HOST_USER = 'root'

# blitz.io server verification for scaling tests
BLITZ_ACCOUNTS = (
    'secret',
    'secret',
)

##Django Compressor Settings
COMPRESS_ENABLED = True
#COMPRESS_PARSER = parser.LxmlParser

from diogenis.settings import INSTALLED_APPS, MIDDLEWARE_CLASSES
DEVELOPER_APPS = (
    'compressor',
)
INSTALLED_APPS += DEVELOPER_APPS

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'TIMEOUT': 6*60*60,
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': '',
#            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

REDIS = redis.Redis(host='localhost', port=6379)
