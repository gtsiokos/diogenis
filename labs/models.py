from django.db import models
from accounts.models import *

class Lesson(models.Model):
	name = models.CharField(max_length=40)
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name

class Lab(models.Model):
	name = models.CharField(max_length=20)
	day = models.CharField(max_length=10)
	hour = models.IntegerField(max_length=2, null=True)

	class Meta:
		ordering = ['name', 'day', 'hour']
	
	def __unicode__(self):
		return u'%s %s %s' % (self.name, self.day, self.hour)

class TeacherToLab(models.Model):
	lesson = models.ForeignKey('Lesson')
	teacher = models.ForeignKey('Teacher')
	lab = models.ForeignKey('Lab')
	
	class Meta:
		ordering = ['lesson']
	
	def __unicode__(self):
		return u'%s - %s [ %s - %s - %s ]' % (self.lesson.name, self.teacher.name, self.lab.name, self.lab.day, self.lab.hour)
		
class StudentToLesson(models.Model):
	student = models.ForeignKey('accounts.AuthStudent')
	lesson = models.ForeignKey('Lesson')
	
	def __unicode__(self):
		return u'%s - %s' % (self.student.user.get_full_name(), self.lesson.name)

class StudentSubscription(models.Model):
	teacher_to_lab = models.ForeignKey('TeacherToLab')
	student = models.ForeignKey('accounts.AuthStudent')
	in_transit = models.BooleanField(default=False)
	
	def __unicode__(self):
		return u'%s [ %s - %s - %s ]' % (self.student.user.get_full_name(), self.teacher_to_lab.lesson.name, self.teacher_to_lab.teacher.name, self.teacher_to_lab.lab.name)

class Teacher(models.Model):
	name = models.CharField(max_length=40)

	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return u'%s' % (self.name)


