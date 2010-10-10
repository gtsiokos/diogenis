#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson

from django.contrib.auth.models import User
from accounts.models import *
from labs.models import *

def user_is_student(user):
	return user.is_authenticated() and not user.get_profile().is_teacher


def excel_api(request):
	results = []
	tmp = []
	the_lessons = Lesson.objects.all()
	the_t2l = TeacherToLab.objects.all()
	for result in the_lessons:
		for t2l_entry in the_t2l:
			if t2l_entry.lesson.name == result.name:
				tmp.append({"name": t2l_entry.teacher.name})
		results.append({"lesson": result.name})#, "professors": {tmp}})
	data = simplejson.dumps(results)
	return HttpResponse(data, mimetype='application/javascript')


@user_passes_test(user_is_student, login_url="/login/")
def display_labs(request, username):
	result = []
	if username == request.user.username:
		q1 = User.objects.get(username=username)
		q2 = AuthStudent()
		for i in AuthStudent.objects.all():
			if i.user.username == q1.username:
				q2 = i
		res1 = StudentSubscription.objects.filter(student=q2)
		res2 = TeacherToLab()
		for j in TeacherToLab.objects.all():
			for i in res1:
				if i.teacher_to_lab==j:
					res2=j
					result.append ({
								"lesson_name":res2.lesson.name,
								"lab_name":res2.lab.name,
								"lab_day":res2.lab.day,
								"lab_hour":res2.lab.hour,
								"teacher":res2.teacher.name
								})
	return render_to_response('students/labs.html', {'results': result}, context_instance = RequestContext(request))
