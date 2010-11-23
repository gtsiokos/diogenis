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

from teachers.helpers import *

def user_is_teacher(user):
	return user.is_authenticated() and user.get_profile().is_teacher


@user_passes_test(user_is_teacher, login_url="/login/")
def manage_labs(request, username):
	if username == request.user.username:
		
		username_hashed = get_hashed_username(request.user.username)
		pending_students_request = request.path.endswith('pending-students/')
		
		q1 = User.objects.get(username=username)
		q2 = u'%s %s' % (q1.last_name, q1.first_name)
		q2 = Teacher.objects.get(name=q2)
		results = []
		my_labs = TeacherToLab.objects.filter(teacher=q2).order_by('lesson')
		
		#####################################################################
		# Ola ta onomata mathimatwn pou mporei na epileksei gia dimiourgia
		# neou ergastiriou o kathigitis. 
		#####################################################################
		I = []
		unique_lessons = []
		for a in my_labs:
			I.append(a.lesson.name)
		my_unique_lessons = set(I)
		for b in my_unique_lessons:
			unique_lessons.append({"name": b})
		
			
		#####################################################################
		# Ola ta onomata mathimatwn, ergastiriwn, oi wres twn ergastiriwn
		# kai oi eggegrammenoi foitites gia to template [teachers/labs.html] 
		#####################################################################		
		for my_lab in my_labs:
			time =  my_lab.lab.hour
			
			if time != 1:
				lesson = my_lab.lesson
				lab = my_lab.lab
			
				data = []
				lab_data = []
				total_labs = TeacherToLab.objects.filter(lesson=lesson, teacher=q2)
			
				total_labs_count = total_labs.count()
				the_labs = total_labs.filter(lab=lab)
			
				for a_lab in the_labs:
					subscriptions = StudentSubscription.objects.filter(teacher_to_lab=my_lab).order_by('student').select_related()
					stud = []
					pending_stud = []
				
					for sub in subscriptions:
						if not sub.in_transit:
							stud.append({
										"first": sub.student.user.first_name,
										"last": sub.student.user.last_name,
										"am": sub.student.am
										})
						elif pending_students_request:
							pending_stud.append({
												"first": sub.student.user.first_name,
												"last": sub.student.user.last_name,
												"am": sub.student.am
												})
				
					lab_time = ("%d μ.μ." % (time-12) if time > 13 else "%d π.μ." % time)
					if time == 12: lab_time = "%d μ.μ." % time
					
					empty_seats = ( my_lab.max_students-len(stud) if stud and my_lab.max_students>len(stud) else 0 )
					
					if pending_students_request:
						if pending_stud:
							data.append({
									"name": lab.name,
									"day": my_lab.lab.day,
									"hour": lab_time,
									"students": pending_stud,
									"empty_seats": empty_seats
									})
					else:
						data.append({
									"name": lab.name,
									"day": my_lab.lab.day,
									"hour": lab_time,
									"students": stud,
									"empty_seats": empty_seats
									})
				
				for s in total_labs:
					time = s.lab.hour
					if time != 1:
						lab_time = ("%d μ.μ." % (time-12) if time > 13 else "%d π.μ." % time)
						if time == 12: lab_time = "%d μ.μ." % time
						stripped_day = s.lab.day[:3]
					
						lab_data.append({
									"name": s.lab.name,
									"day": stripped_day,
									"hour": lab_time
									})
				
				results.append({
							"name": lesson.name,
							"labs_count": total_labs_count,
							"labs": data,
							"labs_list": lab_data,
							})
		
		if request.path.endswith('pending-students/'):
			return render_to_response('teachers/pending_students.html', {'results':results, 'unique_lessons':unique_lessons, 'hash':username_hashed}, context_instance = RequestContext(request))
		else:
			return render_to_response('teachers/labs.html', {'results':results, 'unique_lessons':unique_lessons, 'hash':username_hashed}, context_instance = RequestContext(request))


@user_passes_test(user_is_teacher, login_url="/login/")
def submit_student_to_lab(request, hashed_request):
	
	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "POST" and request.is_ajax():
		
			message = []
			json_data = simplejson.loads(request.raw_post_data)
		
			try:
				new_name = json_data['lnew'][0]['newName']
				new_hour = json_data['lnew'][0]['newHour']
				new_day = json_data['lnew'][0]['newDay']
				old_name = json_data['lold'][0]['oldName']
				old_hour = json_data['lold'][0]['oldHour']
				old_day = json_data['lold'][0]['oldDay']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
		
			check_lab = Lab.objects.filter(day=new_day, hour=new_hour)
			check_t2l = TeacherToLab.objects.filter(lab=check_lab)
			new_lab = Lab.objects.filter(name=new_name, day=new_day, hour=new_hour)
			new_t2l = TeacherToLab.objects.get(lab=new_lab)
			old_lab = Lab.objects.filter(name=old_name, day=old_day, hour=old_hour)
			old_t2l = TeacherToLab.objects.filter(lab=old_lab)
		
		
			if json_data['stud']:
				for student in json_data['stud']:
					check_availability = []
					the_stud = AuthStudent.objects.get(am=student["am"])
					check_availability = StudentSubscription.objects.filter(student=the_stud, teacher_to_lab=check_t2l)
					if not check_availability:
						StudentSubscription.objects.filter(student=the_stud, teacher_to_lab=old_t2l).delete()
						StudentSubscription.objects.create(student=the_stud, teacher_to_lab=new_t2l)
					else:
						msg = u"Κάποιοι σπουδαστές έχουν δηλώσει άλλα εργαστήρια αυτές τις ώρες"
						message.append({ "status": 3, "msg": msg })
			else:
				msg = u"Δεν έχετε επιλέξει κάποιον σπουδαστή"
				message.append({ "status": 3, "msg": msg })
				
			ok_msg = u"Η μεταφορά στο εργαστήριο %s ολοκληρώθηκε" % new_name
			if not message:
				message.append({ "status": 1, "msg": ok_msg })
			data = simplejson.dumps(message)
			return HttpResponse(data, mimetype='application/javascript')
	else:
		return HttpResponse("Atime hax0r, an se vrw tha sou gamisw to kerato...", mimetype="text/plain")


@user_passes_test(user_is_teacher, login_url="/login/")
def add_new_lab(request, hashed_request):

	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "POST" and request.is_ajax():

			message = []
			json_data = simplejson.loads(request.raw_post_data)
			#print json_data;
			
			try:
				action = json_data['newLesson'][0]['action']
				new_day = json_data['newLesson'][0]['newDay']
				new_hour = json_data['newLesson'][0]['newHour']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
			
			
			booked_labs = TeacherToLab.objects.filter(lab__day__contains=new_day).filter(lab__hour=new_hour)
			booked_labs_names = []
			for lab in booked_labs:
				booked_labs_names.append(lab.lab.name)
			open_labs = Lab.objects.exclude(name__in=booked_labs_names).filter(day=new_day).filter(hour=new_hour).select_related()
			
			if action == "getClass":
				if open_labs:
					lab_names = []
					for lab in open_labs:
						lab_names.append({ "name": lab.name })
					
					message.append({ "status": 1, "action": action, "classes": lab_names })
				else:
					msg = u"Δεν υπάρχουν διαθέσιμες αίθουσες για αυτήν την ώρα και ημέρα"
					message.append({ "status": 2, "action": action, "msg": msg })
			elif action == "submitLab":
				try:
					new_name = json_data['newLesson'][0]['newName']
					new_class = json_data['newLesson'][0]['newClass']
					max_students = json_data['newLesson'][0]['maxStudents']
				except KeyError:
					msg = u"Δεν επιλέξατε αίθουσα εργαστηρίου"
					message.append({ "status": 2, "action": action, "msg": msg })
				
				available_lab = open_labs.filter(name=new_class)
				if available_lab:
					try:
						new_lab = Lab.objects.get(name=new_class, day=new_day, hour=new_hour)
						new_lesson = Lesson.objects.get(name=new_name)
						q1 = User.objects.get(username=request.user.username)
						q2 = u'%s %s' % (q1.last_name, q1.first_name)
						new_teacher = Teacher.objects.get(name=q2)
						
						#TeacherToLab.objects.create(lesson=new_lesson, teacher=new_teacher, lab=new_lab, max_students=max_students)
					except:
						msg = u"Παρουσιάστηκε σφάλμα κατά την αποθήκευση των δεδομένων"
						message.append({ "status": 2, "action": action, "msg": msg })
					
					msg = u"Η προσθήκη ολοκληρώθηκε"
					message.append({ "status": 1, "action": action, "msg": msg })
				else:
					msg = u"Σου πήρανε το εργαστήριο μέσα από τα χέρια"
					message.append({ "status": 2, "action": action, "msg": msg })
			
			error_msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
			if not message:
				message.append({ "status": 2, "action": action, "msg": error_msg })
			data = simplejson.dumps(message)
			return HttpResponse(data, mimetype='application/javascript')
	else:
		return HttpResponse("Atime hax0r, an se vrw tha sou gamisw to kerato...", mimetype="text/plain")


@user_passes_test(user_is_teacher, login_url="/login/")
def export_pdf(request, hashed_request):

	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "POST" and request.is_ajax():

			message = []
			json_data = simplejson.loads(request.raw_post_data)
			#print json_data;
			
			try:
				lab_name = json_data['pdfRequest'][0]['labName']
				lab_day = json_data['pdfRequest'][0]['labDay']
				lab_hour = json_data['pdfRequest'][0]['labHour']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
			
			ok_msg = u"Η εξαγωγή ολοκληρώθηκε"
			if not message:
				message.append({ "status": 1, "msg": ok_msg })
			data = simplejson.dumps(message)
			return HttpResponse(data, mimetype='application/javascript')
	else:
		return HttpResponse("Atime hax0r, an se vrw tha sou gamisw to kerato...", mimetype="text/plain")


















