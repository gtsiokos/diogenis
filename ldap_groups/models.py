# -*- coding:utf-8 -*-

from django.contrib.auth.models import Group
from django.db import models

class LDAPGroup(models.Model):
    """
    An LDAPGroup defines a mapping between an LDAP Organizational Unit (OU) and
    a django.contrib.auth.models.Group group. The site admin will create these
    mappings in order to assign various levels of permissions to users who will
    be authenticating via LDAP rather than storing passwords in the Django
    database.  When a user authenticates via LDAP for the first time, the user's
    account in Django will be automatically assigned to the groups mapped by
    this model, and inherit the groups' permissions.
    """
    make_staff = models.BooleanField(default=False)
    make_superuser = models.BooleanField(default=False)
    org_unit = models.CharField(unique=True, max_length=255)
    groups = models.ManyToManyField(Group, related_name='ldap_org_units')
    
    def __unicode__(self):
        return u'LDAP Groups for OU %s' % self.org_unit
    
    class Meta:
        ordering = ['org_unit']
