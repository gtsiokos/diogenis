#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

import os
import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import View
from django.shortcuts import render
from django.utils import simplejson

from django.contrib.auth.models import User
from diogenis.schools.models import *
from diogenis.teachers.models import *
from diogenis.students.models import *

from diogenis.schools.mixins import AuthenticatedSchoolMixin
from diogenis.schools.forms import CoursesUploadForm as Form

class IndexView(AuthenticatedSchoolMixin, View):
    
    def get(self, request, username):
        self.school = School.objects.get(user=request.user)
        return render(request, 'schools/index.html', {})
        
    def post(self, request, username):
        self.school = School.objects.get(user=request.user)
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            form.save(school=self.school)
            msg = u"Η αποθήκευση ολοκληρώθηκε, επιλέξτε τα μαθήματα για τους καθηγητές του τμήματος"
            message = {'status':1, 'msg':msg}
        else:
            msg = u"Το αρχείο που ανεβάσατε δεν είναι τύπου excel"
            message = {'status':2, 'msg':msg}
        
        context = {'message':message}
        return render(request, 'schools/index.html', context)
        
class SubscriptionsActivationView(AuthenticatedSchoolMixin, View):
    
    def post(self, request, username):
        activate = request.POST.get('activate', False)
        request.user.is_active = True if activate else False
        request.user.save()
        
        return HttpResponseRedirect('/')

class ClassroomView(AuthenticatedSchoolMixin, View):
    
    def get(self, request, username):
        self.school = School.objects.get(user=request.user)
        
        if request.is_ajax():
            data = self.get_list_json(request)
            return HttpResponse(data, mimetype='application/javascript')
            
        return render(request, 'schools/classrooms.html', {})
        
    def post(self, request, username, hash_id=None):
        self.school = School.objects.get(user=request.user)
        
        if request.is_ajax():
            if(hash_id):
                data = self.delete_classroom(request)
            else:
                data = self.create_update_classroom(request)
            return HttpResponse(data, mimetype='application/javascript')
        else:
            raise Http404

    def get_list_json(self, request):
        request = request.GET
        response = {}
        try:
            action = request.get('action', '')    #[action] defines different view handling
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        
        classrooms = [classroom.json() for classroom in self.school.classrooms.all().order_by('name')]
        response = {'action':action, 'status':1, 'classrooms':classrooms}
        
        if not response:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        return simplejson.dumps(response)
    
    def create_update_classroom(self, request):
        request = simplejson.loads(request.raw_post_data)
        response = {}
        try:
            action = request['action']    #[action] defines different view handling
            classroom_id = request.get('id', '')
            name = request.get('name', '')
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        
        if classroom_id:
            classroom = Classroom.objects.get(hash_id=classroom_id)
            classroom.name = name if name else classroom.name
            classroom.save()
        else:
            classroom = Classroom(name=name)
            classroom.save()
            self.school.classrooms.add(classroom)
            self.school.save()
        
        if not response:
            msg = u"H αποθήκευση ολοκληρώθηκε"
            response = {'action':action, 'status':1, 'msg':msg}
        return simplejson.dumps(response)
    
    def delete_classroom(self, request):
        request = simplejson.loads(request.raw_post_data)
        response = {}
        try:
            action = request['action']    #[action] defines different view handling
            classroom_id = request.get('id', '')
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        
        classroom = Classroom.objects.get(hash_id=classroom_id)
        many_schools = True if len(classroom.school_set.all())>1 else False
        
        Lab.objects.filter(course__school=self.school, classroom=classroom).delete()
        
        if many_schools:
            self.school.classrooms.remove(classroom)
        else:
            classroom.delete()
        
        if not response:
            msg = u"H διαγραφή ολοκληρώθηκε"
            response = {'action':action, 'status':1, 'msg':msg}
        return simplejson.dumps(response)
    
class TeacherView(AuthenticatedSchoolMixin, View):
    
    def get(self, request, username):
        self.school = School.objects.get(user=request.user)
        
        if request.is_ajax():
            data = self.get_list_json(request)
            return HttpResponse(data, mimetype='application/javascript')
            
        return render(request, 'schools/teachers.html', {})
    
    def post(self, request, username, hash_id=None):
        self.school = School.objects.get(user=request.user)
        
        if request.is_ajax():
            if(hash_id):
                data = self.delete_teacher(request)
            else:
                data = self.create_update_teacher(request)
            return HttpResponse(data, mimetype='application/javascript')
        else:
            raise Http404
    
    def get_list_json(self, request):
        request = request.GET
        response = {}
        try:
            action = request.get('action', '')    #[action] defines different view handling
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        
        teachers = [teacher.json(selected_school=self.school) for teacher in self.school.teacher_set.all().order_by('user__last_name', 'user__first_name')]
        courses = [course.json() for course in Course.objects.filter(school=self.school).select_related()]
        response = {'action':action, 'status':1, 'teachers':teachers, 'courses':courses}
        
        if not response:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        return simplejson.dumps(response)
    
    def create_update_teacher(self, request):
        request = simplejson.loads(request.raw_post_data)
        response = {}
        try:
            action = request['action']    #[action] defines different view handling
            teacher_id = request.get('id', '')
            username = request.get('username', '')
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        
        if teacher_id:
            teacher = Teacher.objects.get(hash_id=teacher_id)
            user = teacher.user
            
            user.username = request.get('username', user.username)
            user.first_name = request.get('firstname', user.first_name)
            user.last_name = request.get('lastname', user.last_name)
            password = request.get('password', '')
            if password: user.set_password(password)
            user.save()
        else:
            try:
                teacher = Teacher.objects.get(user__username=username)
                user = teacher.user
            except:
                user = User()
                
            user.username = request.get('username', '')
            user.first_name = request.get('firstname', '')
            user.last_name = request.get('lastname', '')
            password = request.get('password', '')
            if password: user.set_password(password)
            user.save()
            
            try:
                teacher.schools.add(self.school)
            except:
                teacher = Teacher(user=user)
                teacher.save()
                teacher.schools.add(self.school)
            teacher.save()
        
        for course in request['courses']:
            is_selected = course.get('selected', False)
            course = Course.objects.get(hash_id=course['id'])
            
            labs = Lab.objects.filter(course=course, teacher=teacher)
            if is_selected:
                if not labs:
                    try:
                        lab = Lab(teacher=teacher, course=course, start_hour=1, end_hour=2)
                        lab.save()
                    except Exception, e:
                        print e
                        pass
            else:
                has_already_subscriptions = Subscription.objects.filter(lab__in=labs)
                if has_already_subscriptions:
                    msg = u"O καθηγητής έχει δημιουργήσει εργαστήρια που δεν μπορούν να διαγραφούν"
                    response = {'status':2, 'msg':msg}
                else:
                    labs.delete()
        
        if not response:
            msg = u"H αποθήκευση ολοκληρώθηκε"
            response = {'action':action, 'status':1, 'msg':msg}
        return simplejson.dumps(response)
    
    def delete_teacher(self, request):
        request = simplejson.loads(request.raw_post_data)
        response = {}
        try:
            action = request['action']    #[action] defines different view handling
            teacher_id = request.get('id', '')
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            response = {'status':2, 'msg':msg}
        
        teacher = Teacher.objects.get(hash_id=teacher_id)
        many_schools = True if len(teacher.schools.all())>1 else False
        
        Lab.objects.filter(course__school=self.school, teacher=teacher).delete()
        
        if many_schools:
            teacher.schools.remove(self.school)
        else:
            teacher.user.delete()
        
        if not response:
            msg = u"H διαγραφή ολοκληρώθηκε"
            response = {'action':action, 'status':1, 'msg':msg}
        return simplejson.dumps(response)
        
    
index = IndexView.as_view()
subscriptions_activation = SubscriptionsActivationView.as_view()
classroom = ClassroomView.as_view()
teacher = TeacherView.as_view()
