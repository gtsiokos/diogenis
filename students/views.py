# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson

from django.contrib.auth.models import User
from accounts.models import *
from labs.models import *

from teachers.helpers import get_hashed_username

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
	username_hashed = get_hashed_username(request.user.username)
	
	#import pdb; pdb.set_trace()
	if username == request.user.username:
		q1 = User.objects.get(username=username).get_profile()
		
		unique_lessons = []
		my_lessons = StudentToLesson.objects.filter(student=q1)
		for l in my_lessons:
			unique_lessons.append({"name":l.lesson.name})
		#q2 = AuthStudent()
		#for i in AuthStudent.objects.all():
		#	if i.user.username == q1.username:
		#		q2 = i
		#res1 = StudentSubscription.objects.filter(student=q2)
		#q3 = u'%s %s' % (q1.last_name, q1.first_name)
		#res2 = TeacherToLab()
		#for j in TeacherToLab.objects.all():
		#	for i in res1:
		#		if i.teacher_to_lab==j:
		#			res2=j
		subscriptions = StudentSubscription.objects.filter(student=q1).select_related()
		for subscription in subscriptions:
			result.append ({
							"lesson_name":subscription.teacher_to_lab.lesson.name,
							"lab_name":subscription.teacher_to_lab.lab.name,
							"lab_day":subscription.teacher_to_lab.lab.day,
							"lab_hour":subscription.teacher_to_lab.lab.hour,
							"teacher":subscription.teacher_to_lab.teacher.name,
							})
		return render_to_response('students/labs.html', {'results': result, 'unique_lessons':unique_lessons, 'hash':username_hashed}, context_instance = RequestContext(request))
	else:
		raise Http404


@user_passes_test(user_is_student, login_url="/login/")
def add_new_lab(request, hashed_request):
	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "POST" and request.is_ajax():
			message = []
			json_data = simplejson.loads(request.raw_post_data)
	
			try:
				action = json_data['action']
				lesson = json_data['lesson']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
				
			if action == "getTeachers":
				try:
					lesson = json_data['lesson']
				except KeyError:
					msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
					message.append({ "status": 2, "msg": msg })
					
				available_teachers = TeacherToLab.objects.filter(lesson__name__contains=lesson).order_by('teacher__name').select_related()
				teachers_list = []
				teachers_names = []
				for t in available_teachers:
					if t.teacher.name not in teachers_list:
						teachers_list.append(t.teacher.name)
						teachers_names.append({"name":t.teacher.name})
				#I = []
				#for a in available_teachers:
				#	I.append(a.teacher.name)
				#my_teachers_names = set(I)
				#for b in my_teachers_names:
				#	teachers_names.append({ "name": b })
				message.append({ "status": 1, "action": action, "teachers": teachers_names })
				
				
			data = simplejson.dumps(message)
			return HttpResponse(data, mimetype='application/javascript')
	else:
		return HttpResponse("Atime hax0r, an se vrw tha sou gamisw to kerato...", mimetype="text/plain")
			
			
