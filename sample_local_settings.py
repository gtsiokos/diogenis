# -*- coding: utf-8 -*-

# Sample configuration file for diogenis.teilar.gr website
# Rename to local_settings.py and change accordingly the vars

import os.path

# Change to True for development boxes
DEBUG = True
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

####
#SQLite development database
####
#DATABASES = {
#    'default': {
#        'ENGINE':   'django.db.backends.sqlite3',
#        'NAME':     os.path.join(os.path.dirname(__file__), 'diogenis.db'),
#        'USER':     '',
#        'PASSWORD': '',
#        'HOST':     '',
#        'PORT':     ''
#    }
#}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret'

# Change PROJECT_ROOT to reflect your own dir
PROJECT_ROOT = os.path.dirname(__file__)

# Create a media/ dir for you own static content
# and create an admin_media symlink pointing to django's media
# (admin_media is used for django's admin panel static content)
MEDIA_ROOT = PROJECT_ROOT + '/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'
XLS_ROOT = MEDIA_ROOT+'xls_files/'

##### The following variables can remain unset in development boxes


# used to send mails by sendmail
EMAIL_HOST_USER = 'root'
