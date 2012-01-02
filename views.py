# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib import auth

from diogenis.teachers.models import Teacher
from diogenis.students.models import Student
from diogenis.schools.models import School

def index(request):
    '''
    Handles index page, redirects logged-in users
    '''
    user = request.user
    if user.is_authenticated() and not user.is_superuser:
        try:
            student = Student.objects.get(user=user)
            profile = u'/students/%s/' % user.username
        except:
            try:
                teacher = Teacher.objects.get(user=user)
                profile = '/teachers/%s/' % user.username
            except:
                school = School.objects.get(user=user)
                profile = '/schools/%s/' % user.username
            
        return HttpResponseRedirect(profile)
    else:
        return render(request, 'index.html', {})

