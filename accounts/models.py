from django.db import models
from django.contrib.auth.models import User
     
class UserProfile(models.Model):
    '''
    Creates 1-to-1 relationship with Django User model for adding custom fields.
    
    [URL] http://www.b-list.org/weblog/2006/jun/06/django-tips-extending-user-model/
    '''
    is_teacher = models.BooleanField(default=False)
    user = models.ForeignKey(User, unique=True)

    class Meta:
#        verbose_name = "Subscribed User"
        ordering = ['user']

    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)

class AuthTeacher(UserProfile):
    '''
    Extends UserProfile model for teachers.
    '''
    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)

class AuthStudent(UserProfile):
    '''
    Extends UserProfile model for students.
    
    [am] field is the registration id for every student. 
    '''
    am = models.CharField(max_length=15)
    introduction_year = models.CharField(max_length = 15)
    semester = models.CharField(max_length = 2)

    class Meta:
        ordering = ['am']
    
    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)



