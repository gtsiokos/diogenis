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

from teachers.helpers import get_hashed_username, humanize_time, get_lab_hour, set_hour_range, pdf_exporter

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
		my_labs = my_labs.filter(lab__start_hour__gt=1)
		for my_lab in my_labs:
			hour = get_lab_hour(my_lab.lab)
			
			lesson = my_lab.lesson
			lab = my_lab.lab
			data = []
			lab_data = []
			
			total_labs = TeacherToLab.objects.filter(lesson=lesson, teacher=q2, lab__start_hour__gt=1).order_by('lab__start_hour')
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
			new_hour = set_hour_range(1,1)
			json_data = simplejson.loads(request.raw_post_data)
			#print json_data;
			
			try:
				action = json_data['action']
				new_day = json_data['newDay']
				new_hour['start'] = json_data['newHour']['start']
				new_hour['end'] = json_data['newHour']['end']
			except KeyError:
				msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
				message.append({ "status":2, "msg":msg })
			
			if action == "getClass":
				if new_hour['start'] >= new_hour['end']:
					msg = u"H ώρα έναρξης του εργαστηρίου είναι μεγαλύτερη της ώρας λήξης"
					message.append({ "status":2, "action":action, "msg":msg })
				else:
					unique_labs = []
					lab_names = []
					#new_lab = Lab(day=new_day, start_hour=new_hour['start'], end_hour=new_hour['end'])
					labs = Lab.objects.filter(day__contains=new_day)
					#available_labs = Lab.get_available_labs(new_lab=new_lab)
					for lab in labs:
						if lab.name not in lab_names:
							lab_names.append(lab.name)
							unique_labs.append({ "name": lab.name })
					message.append({ "status":1, "action":action, "classes":unique_labs })
				
			elif action == "submitLab":
				try:
					new_name = json_data['newName']
					new_class = json_data['newClass']
					max_students = json_data['maxStudents']
				except KeyError:
					msg = u"Δεν επιλέξατε αίθουσα εργαστηρίου"
					message.append({ "status":2, "action":action, "msg":msg })
				
				new_lab = Lab(name=new_class, day=new_day, start_hour=new_hour['start'], end_hour=new_hour['end'])
				no_conflict = Lab.check_conflict(new_lab=new_lab)
				if no_conflict and new_hour['start'] < new_hour['end']:
					try:
						q1 = User.objects.get(username=request.user.username)
						q2 = u'%s %s' % (q1.last_name, q1.first_name)
						new_teacher = Teacher.objects.get(name=q2)
						new_lesson = Lesson.objects.get(name=new_name)
						
						new_lab.save()
						TeacherToLab(lesson=new_lesson, teacher=new_teacher, lab=new_lab, max_students=max_students).save()
					except:
						msg = u"Παρουσιάστηκε σφάλμα κατά την αποθήκευση των δεδομένων"
						message.append({ "status":2, "action":action, "msg":msg })
					
					msg = u"Η προσθήκη ολοκληρώθηκε"
					message.append({ "status":1, "action":action, "msg":msg })
				else:
					msg = u"Η αίθουσα δεν είναι διαθέσιμη"
					message.append({ "status":2, "action":action, "msg":msg })
			
			error_msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
			if not message:
				message.append({ "status":2, "action":action, "msg":error_msg })
			data = simplejson.dumps(message)
			return HttpResponse(data, mimetype='application/javascript')
	else:
		return HttpResponse("Atime hax0r, an se vrw tha sou gamisw to kerato...", mimetype="text/plain")


@user_passes_test(user_is_teacher, login_url="/login/")
def export_pdf(request, hashed_request, name, day, start_hour, end_hour):
	username_hashed = get_hashed_username(request.user.username)
	
	if username_hashed == hashed_request:
		if request.method == "GET":
			hour = set_hour_range(start_hour, end_hour)
			
			labtriplet = [name, day, hour]
			
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


















