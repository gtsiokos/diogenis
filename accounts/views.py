# -*- coding: utf-8 -*-

messages = []

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth

from django.contrib.auth.models import User
from diogenis.accounts.models import *
from diogenis.labs.models import *

from diogenis.accounts.forms import *
from diogenis.accounts.dionysos import get_student_credentials


def login(request):
	'''
	Authenticates username and password, creates a session and redirects user to the respective page.
	'''
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('username') and post.has_key('password'):
			usr = post['username']
			pwd = post['password']
			remember = False
			if post.has_key('remember'):
				remember = True
			user = auth.authenticate(username=usr, password=pwd)
			if user is not None and user.is_active:
				auth.login(request, user)
				if user.is_superuser:
					return HttpResponseRedirect('/system/admin/')
				if remember==False:
					request.session.set_expiry(0)
				if user.get_profile().is_teacher:
					return HttpResponseRedirect('/teachers/'+user.username+'/')
				else:
					return HttpResponseRedirect('/students/'+user.username+'/')
			else:
				return render_to_response('index.html', {'message':'Δεν ανοίκεις στο μαγικό Teilar, φύγε όσο είναι καιρός'}, context_instance = RequestContext(request))
			
	return render_to_response('accounts/login.html', {}, context_instance = RequestContext(request))


def logout(request):
	'''
	Logs out user
	'''
	auth.logout(request)
	return HttpResponseRedirect('/')


def signup(request):
	'''
	Signup form for students.
	
	Uses get_student_credentials for retrieving student's data from dionysos.teilar.gr
	Uses get_create_student for saving new student user and redirects him to the respective page.
	'''
	global messages
	messages = []
	
	if request.method == 'POST':
		form = StudentSignupForm(request.POST)
		if form.is_valid():
			credentials = get_student_credentials(request.POST.get('dionysos_username'), request.POST.get('dionysos_password'))
			if credentials:
				user = get_create_student(credentials)
				if user is not None and user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect('/students/'+user.username+'/')
			else:
				msg = u"Παρουσιάστηκε σφάλμα στον Διόνυσο"
				message.append({"status": 2, "msg": msg})
	else:
		form = StudentSignupForm()
	
	context = {'form':form, 'messages':messages}
	return render_to_response('accounts/signup.html', context, context_instance = RequestContext(request))


def get_create_student(credentials):
	'''
	Saves new User and his profile with extended data.
	Saves relations with existing lessons retrieved by dionysos.teilar.gr
	
	Returns: User object || None (if User already exists)
	'''
	global messages

	try:
		user = User(
			username = credentials['username'],
			first_name = credentials['first_name'],
			last_name = credentials['last_name'],
			email = credentials['username'] + '@emptymail.com'
		)
		user.is_staff = False
		user.is_superuser = False
		user.set_password(credentials['password'])
		user.save()

		user_profile = AuthStudent(
			user = user,
			is_teacher = False,
			am = credentials['registration_number'],
			introduction_year = credentials['introduction_year'],
			semester = credentials['semester']
		)	
		user_profile.save()

	 
		if credentials.has_key('labs'):
			for lab in credentials['labs']:
				try:
					student_lesson = StudentToLesson(
													student = user_profile,
													lesson = Lesson.objects.get(name = lab)
													)
					student_lesson.save()
				except Exception as e:
					#################
					# Logging needed
					#################
					print u'##############'
					print e
					print u'##############'
					pass
	
		return user
	except:
		msg = u"Έχετε κάνει εγγραφή, δοκιμάστε να κάνετε login με τα στοιχεία σας"
		messages.append({"status": 1, "msg": msg})
		return None


