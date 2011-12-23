#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from diogenis.students.models import Student

def user_is_student(user):
    try:
        request_user = Student.objects.get(user=user)
        return user.is_authenticated() and not request_user.is_school and not request_user.is_teacher
    except:
        return False

class AuthenticatedStudentMixin(object):
    
    @method_decorator(user_passes_test(user_is_student, login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if username != request.user.username: raise Http404
        return super(AuthenticatedStudentMixin, self).dispatch(request, *args, **kwargs)
