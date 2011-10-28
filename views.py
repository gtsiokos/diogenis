# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib import auth

from redis.exceptions import ResponseError

from diogenis.teachers.models import Teacher
from diogenis.students.models import Student
from diogenis.schools.models import School

def index(request):
    '''
    Handles index page, redirects logged-in users
    '''
    try:
        user = request.user
    except ResponseError:
        user = request.user
    if user.is_authenticated and user.is_active and user is not None and not user.is_superuser:
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

