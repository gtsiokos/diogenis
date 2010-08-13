#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import e10

from django.contrib.auth.models import User

from accounts.models import *
from labs.models import *


def manage_db(request):
	return render_to_response('labs/manage_db.html', {}, context_instance = RequestContext(request))

def save_db(request):
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
#					teacher = Teacher(teachname=k)
#					teacher.save()
#					teacher.labs.add(labname)
		msg = 'Η μεταφορά του αρχείου Excel ολοκληρώθηκε.'
	else:
		raise Http404
	return render_to_response('labs/manage_db.html', {'msg': msg}, context_instance = RequestContext(request))
	
def fill_labs(request):
	try:
		e10.fill_labs()
		msg='Ο πίνακας Labs συμπληρώθηκε.'
	except:
		msg='Παρουσιάστηκε Σφάλμα.'
	return render_to_response('labs/manage_db.html', {'msg': msg}, context_instance = RequestContext(request))



