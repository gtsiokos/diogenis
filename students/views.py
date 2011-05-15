# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson

from django.contrib.auth.models import User
from diogenis.accounts.models import *
from diogenis.labs.models import *

from diogenis.common.helpers import humanize_time, set_hour_range
from diogenis.labs.helpers import get_lab_hour

def user_is_student(user):
	return user.is_authenticated() and not user.get_profile().is_teacher


def excel_api(request):
	'''
	For testing purposes, not implemented
	'''
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
	'''
	Manages student's view.
	
	Handling Template:	/students/labs.html
	'''
	result = []
	if username == request.user.username:
		q1 = User.objects.get(username=username).get_profile()
		
		unique_lessons = []		#contains lesson names related to the student.
		my_lessons = StudentToLesson.objects.filter(student=q1).order_by('lesson__name')
		for l in my_lessons:
			unique_lessons.append({"name":l.lesson.name})
		
		subscriptions = StudentSubscription.objects.filter(student=q1).select_related()
		for subscription in subscriptions:
			result.append ({
							"lesson_name":subscription.teacher_to_lab.lesson.name,
							"lab_name":subscription.teacher_to_lab.lab.name,
							"lab_day":subscription.teacher_to_lab.lab.day,
							"lab_hour":get_lab_hour(subscription.teacher_to_lab.lab),
							"lab_start_hour":humanize_time(subscription.teacher_to_lab.lab.start_hour),
							"lab_end_hour":humanize_time(subscription.teacher_to_lab.lab.end_hour),
							"teacher":subscription.teacher_to_lab.teacher.name,
							})
		return render_to_response('students/labs.html', {'results': result, 'unique_lessons':unique_lessons}, context_instance = RequestContext(request))
	else:
		raise Http404


@user_passes_test(user_is_student, login_url="/login/")
def add_new_lab(request):
	'''
	Manages JSON request for lab subscription.
	
	Client-side: [js/core.students.lab.register.js]
	'''
	if request.method == "POST" and request.is_ajax():
		message = []
		json_data = simplejson.loads(request.raw_post_data)

		try:
			action = json_data['action']	#[action] defines different view handling
		except KeyError:
			msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
			message.append({ "status": 2, "msg": msg })
			
		if action == "getTeachers":			#returns available teachers for the requested lesson
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
			
			message.append({ "status": 1, "action": action, "teachers": teachers_names })
		
		if action == "getClasses":			#returns available classes for the requested lesson,teacher
			try:
				lesson = json_data['lesson']
				teacher = json_data['teacher']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
			
			available_labs = TeacherToLab.objects.filter(lesson__name__contains=lesson, teacher__name__contains=teacher, lab__start_hour__gt=1).order_by('lab__day', 'lab__start_hour').select_related()
			
			if available_labs:				#checks whether requested teacher has registered labs
				classes_list = []
				for l in available_labs:
					class_start_time = humanize_time(l.lab.start_hour)
					class_end_time = humanize_time(l.lab.end_hour)
					classes_list.append({"name":l.lab.name,"day":l.lab.day, "start_hour":class_start_time, "end_hour":class_end_time, "start_hour_raw":l.lab.start_hour, "end_hour_raw":l.lab.end_hour })
				
				message.append({ "status": 1, "action": action, "classes": classes_list })
			else:
				msg = u"Ο καθηγητής που επιλέξατε δεν έχει δημοσιεύσει τα εργαστήρια του στον Διογένη"
				message.append({ "status": 2, "action": action, "msg": msg })
		
		if action == "checkAvailability" or action == "submitLab":			#common processes done by these actions
			try:
				lesson = json_data['lesson']
				teacher = json_data['teacher']
				class_name = json_data['name']
				class_day = json_data['day']
				class_hour = set_hour_range(json_data['start_hour'], json_data['end_hour'])
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
			
			lab_available = False
			try:
				unique_class = TeacherToLab.objects.get(lesson__name__contains=lesson, teacher__name__contains=teacher, lab__name__contains=class_name, lab__day__contains=class_day, lab__start_hour=class_hour['start'], lab__end_hour=class_hour['end'])
				students_count = StudentSubscription.objects.filter(teacher_to_lab=unique_class).count()
				available_seats = unique_class.max_students - students_count
				lab_available = (True if available_seats > 0 else False)	#if the requested lab has available seats
			except:
				msg = u"Το εργαστήριο που ζητήσατε δεν βρέθηκε"
				message.append({ "status": 2, "action": action, "msg": msg })
				
		
		if action == "checkAvailability":									#prompts user to verify a pending subscription in case lab is full
			if lab_available:
				message.append({ "status": 1, "action": action })
			else:
				msg = u"To εργαστήριο %s δεν έχει ελεύθερες θέσεις. Θέλετε να υποβάλεται αίτημα στον καθηγητή για την έγκριση της εγγραφή σας?" % class_name
				message.append({ "status": 3, "action": action, "msg": msg })
		
		if action == "submitLab":
			the_student = AuthStudent.objects.get(user=request.user)
			try:
				already_subscribed = StudentSubscription.objects.get(student=the_student, teacher_to_lab__lesson__name=lesson)
				msg = u"Έχετε ήδη εγγραφεί στο συγκεκριμένο μάθημα"
				message.append({ "status": 2, "action": action, "msg": msg })
			except:
				if lab_available:											#subscription completed
					StudentSubscription.objects.create(student=the_student, teacher_to_lab=unique_class)
					msg = u"Η εγγραφή σας στο εργαστήριο %s ολοκληρώθηκε" % class_name
				else:														#pending subscription completed
					StudentSubscription.objects.create(student=the_student, teacher_to_lab=unique_class, in_transit=True)
					msg = u"Στείλαμε το αίτημα σας στον καθηγητή"
				message.append({ "status": 1, "action": action, "msg": msg })
		
		error_msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
		if not message:
			message.append({ "status": 2, "msg": error_msg })
		data = simplejson.dumps(message)
		return HttpResponse(data, mimetype='application/javascript')
		
			
