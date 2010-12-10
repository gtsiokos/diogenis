#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
import e10

from django.contrib.auth.models import User
from accounts.models import *
from labs.models import *

def user_is_superuser(user):
	return user.is_superuser


@user_passes_test(user_is_superuser, login_url="/login/")
def control_panel(request):

	message = []
	if request.method == "POST":

		Teacher.objects.all().delete()
		Lesson.objects.all().delete()
		TeacherToLab.objects.all().delete()
		Lab.objects.all().delete()

		k=''
		kk=''
		temp=[]
		splitname=''
		labname=''
		teachname=''
		temp=e10.xls_rdr()
		
		empty_lab = Lab(name='', day='', hour=1)
		empty_lab.save()

		for k in temp:
			if k.startswith('-'):
				labname=''
				splitname=k.split()
				for kk in splitname[1:-1]:
					labname = labname+kk+' '
				labname = labname[0:len(labname)-1]
				labname = Lesson(name=labname)
				labname.save()

			else:
				my_teacher = Teacher.objects.filter(name=k)
				
				if my_teacher:
					tch = Teacher.objects.get(name=k)
					a = TeacherToLab(teacher=tch, lesson=labname, lab=empty_lab)
					a.save()
				else:
					b = Teacher(name=k)
					b.save()
					c = TeacherToLab(teacher=b, lesson=labname, lab=empty_lab)
					c.save()
		
		try:
			e10.fill_labs()
		except:
			msg= u'Παρουσιάστηκε Σφάλμα'
			message.append({ "status": 2, "msg": msg })
			
		ok_msg = u"Η μεταφορά του αρχείου Excel ολοκληρώθηκε"
		if not message:
			message.append({ "status": 1, "msg": ok_msg })
#	else:
#		raise Http404
	return render_to_response('system/cpanel.html', {'message': message}, context_instance = RequestContext(request))



