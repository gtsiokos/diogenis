# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth

def index(request):
    '''
    Handles index page, redirects logged-in users
    '''
    user = request.user
    if user.is_authenticated and user.is_active and user is not None:
        if user.is_superuser:
            return HttpResponseRedirect('/system/admin/')
        if user.get_profile().is_teacher:
            return HttpResponseRedirect('/teachers/'+user.username+'/')
        else:
            return HttpResponseRedirect('/students/'+user.username+'/')
    else:
        return render_to_response('index.html', {}, context_instance = RequestContext(request))


