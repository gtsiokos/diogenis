#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from django.db import models
from django import forms

from diogenis.accounts.models import *

class UploadPdf(forms.Form):
    file  = forms.FileField()

class Lesson(models.Model):
	name = models.CharField(max_length=40)
	
	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return self.name

class Classroom(models.Model):
	name = models.CharField(max_length=20)
	
	class Meta:
		verbose_name = "Αίθουσα"
		verbose_name_plural = "Αίθουσες"
		ordering = ['name']
		
	def __unicode__(self):
		return self.name

class Lab(models.Model):
	name = models.CharField(max_length=20)
	day = models.CharField(max_length=10)
	#hour = models.IntegerField(max_length=2)
	start_hour = models.IntegerField(max_length=2)
	end_hour = models.IntegerField(max_length=2)

	class Meta:
		ordering = ['name', 'day', 'start_hour']
	
	def __unicode__(self):
		return u'%s %s [%s - %s]' % (self.name, self.day, self.start_hour, self.end_hour)
	
	@classmethod
	def check_conflict(self, *args, **kwargs):
		new_lab = kwargs.get('new_lab')
		
		start = new_lab.start_hour
		end = new_lab.end_hour
		labs = Lab.objects.filter(day__contains=new_lab.day, name__contains=new_lab.name, start_hour__gt=1)
		#print labs
		flag = -1
		if labs:
			for lab in labs:
				if (( (start > lab.end_hour) or (start == lab.end_hour) ) or ( (end == lab.start_hour) or (end < lab.start_hour) )):
					a = 2
				else:
					flag = 0
		
		return False if flag==0 else True
		
#	@classmethod
#	def get_available_labs(self, *args, **kwargs):
#		new_lab = kwargs.get('new_lab')
#		
#		start = new_lab.start_hour
#		end = new_lab.end_hour
#		labs = Lab.objects.filter(day__contains=new_lab.day)
#		available_labs = []
#		
#		
#		if labs:
#			for lab in labs:
#				print lab.name
#				if (( (start > lab.end_hour) or (start == lab.end_hour) ) or ( (end == lab.start_hour) or (end < lab.start_hour) )):
#					available_labs.append(lab)
#		
#		return available_labs
		
class TeacherToLab(models.Model):
	lesson = models.ForeignKey('Lesson')
	teacher = models.ForeignKey('Teacher')
	lab = models.ForeignKey('Lab')
	max_students = models.IntegerField(max_length=2, null=True, blank=True)
	
	class Meta:
		ordering = ['lesson']
	
	def __unicode__(self):
		return u'%s - %s [ %s - %s (%s - %s) ]' % (self.lesson.name, self.teacher.name, self.lab.name, self.lab.day, self.lab.start_hour, self.lab.end_hour)
		
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
	
	@classmethod
	def check_availability(self, *args, **kwargs):
		new_t2l = kwargs.get('new_t2l')
		student = kwargs.get('student')
		
		name = new_t2l.lab.name
		day = new_t2l.lab.day
		start = new_t2l.lab.start_hour
		end = new_t2l.lab.end_hour
		current_subscriptions = StudentSubscription.objects.filter(student=student, teacher_to_lab__lab__day__contains=day, in_transit=False).select_related()
		
		flag = -1
		if current_subscriptions:
			for cs in current_subscriptions:
				if (( (start > cs.teacher_to_lab.lab.end_hour) or (start == cs.teacher_to_lab.lab.end_hour) ) or ( (end == cs.teacher_to_lab.lab.start_hour) or (end < cs.teacher_to_lab.lab.start_hour) )):
					a = 2
				else:
					flag = 0
		
		return False if flag==0 else True
	
class Teacher(models.Model):
	name = models.CharField(max_length=40)

	class Meta:
		ordering = ['name']
	
	def __unicode__(self):
		return u'%s' % (self.name)


