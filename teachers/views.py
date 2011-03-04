#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

import os
import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson

from django.contrib.auth.models import User
from accounts.models import *
from labs.models import *

from teachers.helpers import get_hashed_username, humanize_time, get_lab_hour, pdf_exporter

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
		my_labs = TeacherToLab.objects.filter(teacher=q2).order_by('lesson__name', 'lab__start_hour').select_related()
		
		#####################################################################
		# To unique_lessons periexei ola ta onomata mathimatwn pou mporei
		# na epileksei o kathigitis gia dimiourgia neou ergastiriou se
		# alphabitiki seira.
		#####################################################################
		unique_lessons = []
		labs_list = []
		for my_lab in my_labs:
			if my_lab.lesson.name not in labs_list:
				labs_list.append(my_lab.lesson.name)
				unique_lessons.append({"name": my_lab.lesson.name})
			
		#####################################################################
		# Ola ta onomata mathimatwn, ergastiriwn, oi wres twn ergastiriwn
		# kai oi eggegrammenoi foitites gia to template [teachers/labs.html] 
		#####################################################################		
		my_labs = my_labs.filter(lab__hour__gt=1)
		for my_lab in my_labs:
			hour = get_lab_hour(my_lab.lab)
			
			lesson = my_lab.lesson
			lab = my_lab.lab
			data = []
			lab_data = []
			
			total_labs = TeacherToLab.objects.filter(lesson=lesson, teacher=q2, lab__hour__gt=1).order_by('lab__start_hour')
			total_labs_count = total_labs.count()
			the_labs = total_labs.filter(lab=lab)
			
			start_hour_raw = my_lab.lab.start_hour
			end_hour_raw = my_lab.lab.end_hour
			
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
				
				empty_seats = ( my_lab.max_students-len(stud) if stud and my_lab.max_students>len(stud) else 0 )
				
				if pending_students_request:
					if pending_stud:
						data.append({
								"name": lab.name,
								"day": my_lab.lab.day,
								"hour": hour,
								"students": pending_stud,
								"empty_seats": empty_seats
								})
				else:
					data.append({
								"name": lab.name,
								"day": my_lab.lab.day,
								"hour": hour,
								"students": stud,
								"empty_seats": empty_seats
								})
			
			for s in total_labs:
				hour = get_lab_hour(s.lab)
				stripped_day = s.lab.day[:3]
			
				lab_data.append({
							"name": s.lab.name,
							"day": stripped_day,
							"hour": hour
							})
			
			results.append({
						"name": lesson.name,
						"labs_count": total_labs_count,
						"labs": data,
						"labs_list": lab_data,
						})
		
		context = {'results':results, 'unique_lessons':unique_lessons, 'hash':username_hashed}
		template_to_render = ('teachers/pending_students.html' if pending_students_request else 'teachers/labs.html')
		return render_to_response(template_to_render, context, context_instance = RequestContext(request))
	else:
		raise Http404


@user_passes_test(user_is_teacher, login_url="/login/")
def submit_student_to_lab(request, hashed_request):
	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "POST" and request.is_ajax():
		
			message = []
			json_data = simplejson.loads(request.raw_post_data)
		
			try:
				new_name = json_data['lnew']['newName']
				new_hour = json_data['lnew']['newHour']
				new_day = json_data['lnew']['newDay']
				old_name = json_data['lold']['oldName']
				old_hour = json_data['lold']['oldHour']
				old_day = json_data['lold']['oldDay']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status": 2, "msg": msg })
			
			new_lab = Lab.objects.filter(name=new_name, day=new_day, start_hour=new_hour['start'], end_hour=new_hour['end'])
			new_t2l = TeacherToLab.objects.get(lab=new_lab)
			old_lab = Lab.objects.filter(name=old_name, day=old_day, start_hour=old_hour['start'], end_hour=old_hour['end'])
			old_t2l = TeacherToLab.objects.filter(lab=old_lab)
			
			try:
				students = json_data['stud']
				empty_test = students[0]
				for student in students:
					stud = AuthStudent.objects.get(am=student['am'])
					available = StudentSubscription.check_availability(student=stud, new_t2l=new_t2l)
					if available:
						StudentSubscription.objects.filter(student=stud, teacher_to_lab=old_t2l).delete()
						StudentSubscription.objects.create(student=stud, teacher_to_lab=new_t2l)
					else:
						msg = u"Κάποιοι σπουδαστές έχουν δηλώσει άλλα εργαστήρια αυτές τις ώρες"
						message.append({ "status": 3, "msg": msg })
			except:
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
						
						TeacherToLab.objects.create(lesson=new_lesson, teacher=new_teacher, lab=new_lab, max_students=max_students)
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
def export_pdf(request, hashed_request, class_name, day, hour):
	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "GET":

			labtriplet = [class_name, day, hour]
			
			username = request.user.username
			username = User.objects.get(username=username)
			username = u'%s %s' % (username.last_name, username.first_name)
			
			a=datetime.datetime.now()
			tempname = str('teachers/%s.pdf') % (a)
			tempname = unicode(tempname,"utf-8")
			
			response = HttpResponse(mimetype='application/pdf')
			response['Content-Disposition'] = 'attachment; filename=%s' % (tempname)
			pdf_exporter(labtriplet,response)
			return response
			os.remove("temp.pdf")
	else:
		return HttpResponse("Atime hax0r, an se vrw tha sou gamisw to kerato...", mimetype="text/plain")


















