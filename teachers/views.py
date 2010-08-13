#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from accounts.models import *
from labs.models import *

def user_is_teacher(user):
	return user.is_authenticated() and user.get_profile().is_teacher

@user_passes_test(user_is_teacher, login_url="/login/")
def labs(request, username):
	q1 = User.objects.get(username=username)
	q2 = u'%s %s' % (q1.last_name, q1.first_name)
	q2 = Teacher.objects.get(name=q2)
#	qq2 = Lab.objects.get(day='')
#	qq3 = Lesson.objects.get(name='ΑΣΦΑΛΕΙΑ ΠΛΗΡΟΦΟΡΙΑΚΩΝ ΣΥΣΤΗΜΑΤΩΝ')
	results = TeacherToLab.objects.filter(teacher=q2)
	
	return render_to_response('teachers/labs.html', {'results': results}, context_instance = RequestContext(request))

