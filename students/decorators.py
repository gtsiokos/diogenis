#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
from django.shortcuts import render

from diogenis.students.models import Student

def student_has_subscriptions_enabled(view_func):
    """
    Decorator checks whether subscriptions are activated by school. 
    """
    
    def decorator(request, *args, **kwargs):
        schools = Student.objects.get(user=request.user).schools.all()
        school_is_active = schools[0].user.is_active
        
        if school_is_active:
            response = view_func(request, *args, **kwargs)
        else:
            response = render(request, 'index.html', {'message':u'Οι δηλώσεις εργαστηρίων έχουν απενεργοποιηθεί μέχρι την επίσημη \
                                                                μέρα έναρξης εγγραφών σύμφωνα με τις ανακοινώσεις του τμήματος'})
        return response
    
    return decorator

