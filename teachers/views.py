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
		
		q1 = User.objects.get(username=username)
		q2 = u'%s %s' % (q1.last_name, q1.first_name)
		q2 = Teacher.objects.get(name=q2)
		results = []
		tmp = "random string"
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
					subscriptions = StudentSubscription.objects.filter(teacher_to_lab=my_lab, in_transit=False).order_by('student').select_related()
					stud = []
				
					for sub in subscriptions:
						stud.append({	"first": sub.student.user.first_name,
									"last": sub.student.user.last_name,
									"am": sub.student.am
									})
				
					lab_time = ("%d μ.μ." % (time-12) if time > 13 else "%d π.μ." % time)

					data.append({	"name": lab.name,
								"day": my_lab.lab.day,
								"hour": lab_time,
								"students": stud
								})
				
				for s in total_labs:
					time = s.lab.hour
					lab_time = ("%d μ.μ." % (time-12) if time > 13 else "%d π.μ." % time)

					stripped_day = s.lab.day[:3]
					

					lab_data.append({
								"name": s.lab.name,
								"day": stripped_day,
								"hour": lab_time
								})
				
				
				if tmp == lesson.name:
					results.append({
								"labs_count": total_labs_count,
								"labs": data,
								"labs_list": lab_data,
								})
				else:
					results.append({
								"name": lesson.name,
								"labs_count": total_labs_count,
								"labs": data,
								"labs_list": lab_data,
								})
					tmp = lesson.name
				
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
				msg = u"Υπήρχε σφάλμα κατά την μεταφορά του μηνύματος"
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
						StudentSubscription.objects.create(student=the_stud, teacher_to_lab=new_t2l).save()
						StudentSubscription.objects.filter(student=the_stud, teacher_to_lab=old_t2l).delete()
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
def add_new_lab(request):
	if request.method == "POST":
		if request.is_ajax():
			
			message = []
			json_data = simplejson.loads(request.raw_post_data)
			
			data = simplejson.dumps(message)
			return HttpResponse(data, mimetype='application/javascript')

























