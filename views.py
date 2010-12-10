#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.contrib import auth

def index(request):
	return render_to_response('index.html', {}, context_instance = RequestContext(request))
	
def login(request):
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
			
	return render_to_response('login.html', {}, context_instance = RequestContext(request))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')
