from django.db import models
from django.contrib.auth.models import User
     
class UserProfile(models.Model):
	is_teacher = models.BooleanField(default=False)
	user = models.ForeignKey(User, unique=True)

	class Meta:
#		verbose_name = "Subscribed User"
		ordering = ['user']

	def __unicode__(self):
		return u'%s %s' % (self.user.last_name, self.user.first_name)

class AuthTeacher(UserProfile):
	is_gtp = models.BooleanField(default=True)
	
	def __unicode__(self):
		return u'%s  f %s' % (self.user.last_name, self.user.first_name)


class AuthStudent(UserProfile):
	is_tourist = models.BooleanField(default=True)
	
	def __unicode__(self):
		return u'%s %s' % (self.user.last_name, self.user.first_name)
