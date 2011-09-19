#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    '''
    Creates 1-to-1 relationship with Django User model for adding custom fields.
    
    [URL] http://www.b-list.org/weblog/2006/jun/06/django-tips-extending-user-model/
    '''
    user = models.ForeignKey(User, unique=True)
    is_teacher = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        ordering = ['user']

    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)
