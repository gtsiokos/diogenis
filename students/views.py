#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import View
from django.shortcuts import render
from django.utils import simplejson

from diogenis.students.models import *
from diogenis.teachers.models import *
from diogenis.schools.models import *

from diogenis.common.decorators import request_passes_test, cache_view
from diogenis.students.decorators import student_has_subscriptions_enabled
from diogenis.auth.dionysos import DionysosAuthentication
from diogenis.students.mixins import AuthenticatedStudentMixin

def user_is_student(request, username=None, **kwargs):
    try:
        user = request.user
        student = Student.objects.get(user=user)
        if username:
            return user.is_authenticated() and username == user.username
        return user.is_authenticated()
    except:
        return False

@request_passes_test(user_is_student, login_url='/login/')
@student_has_subscriptions_enabled
@cache_view(48*60*60)
def display_labs(request, username):
    '''
    Manages student's view.
    
    Handling Template:    /students/labs.html
    '''
    student = Student.objects.get(user=request.user)
    
    courses = student.get_courses_by_school()
    subscriptions = student.get_subscriptions()
    
    context =   {
                'subscriptions':subscriptions['context'],
                'courses':courses['context']
                }
    return render(request, 'students/labs.html', context)


@request_passes_test(user_is_student, login_url='/login/')
def add_new_lab(request):
    '''
    Manages JSON request for lab subscription.
    
    Client-side: [js/core.students.lab.register.js]
    '''
    if request.method == 'POST' and request.is_ajax():
        json_data = simplejson.loads(request.raw_post_data)
        data = {}
        
        student = Student.objects.get(user=request.user)
        schools = student.schools.all()
        
        try:
            action = json_data['action']    #[action] defines different view handling
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            data = {'status':2, 'msg':msg}
            
        if action == "teachers":            #returns available teachers for the requested lesson
            try:
                course_id = json_data['course_id']
            except KeyError:
                msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
                data = {'status':2, 'msg':msg}
            available_teachers = Lab.objects.filter(course__school__in = schools, course__hash_id=course_id).order_by('teacher').select_related()
            teachers_list = []
            teachers = []
            for available_teacher in available_teachers:
                teacher_name = available_teacher.teacher.user.get_full_name()
                teacher_id = available_teacher.teacher.hash_id
                if teacher_name not in teachers_list:
                    teachers_list.append(teacher_name)
                    teachers.append({'name':teacher_name, 'id':teacher_id})
            
            data = {'status':1, 'action':action, 'teachers':teachers}
        
        if action == "classes":            #returns available classes for the requested lesson,teacher
            try:
                course_id = json_data['course_id']
                teacher_id = json_data['teacher_id']
            except KeyError:
                msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
                data = {'status':2, 'msg':msg}
            
            available_labs = Lab.objects.filter(course__hash_id=course_id, course__school__in = schools, teacher__hash_id=teacher_id, start_hour__gt=1).order_by('day', 'start_hour').select_related()
            
            if available_labs:                #checks whether requested teacher has registered labs
                classes_list = []
                for lab in available_labs:
                    hour = lab.hour
                    classes_list.append({'id':lab.hash_id, 'lesson':lab.course.lesson.name, 'day':lab.day, 'start_hour':hour['start']['humanized'], 'end_hour':hour['end']['humanized'] })
                
                data = {'status':1, 'action':action, 'classes':classes_list}
            else:
                msg = u"Ο καθηγητής που επιλέξατε δεν έχει δημοσιεύσει τα εργαστήρια του στον Διογένη"
                data = {'status':2, 'action':action, 'msg':msg}
        
        if action == "availability" or action == "submit":            #common processes done by these actions
            try:
                lab_id = json_data['lab_id']
            except KeyError:
                msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
                data = {'status':2, 'msg':msg}
            
            lab_available = False
            try:
                lab = Lab.objects.get(hash_id=lab_id)
                lab_available = (True if lab.empty_seats > 0 else False)    #if the requested lab has available seats
            except:
                msg = u"Το εργαστήριο που ζητήσατε δεν βρέθηκε"
                data = {'status':2, 'action':action, 'msg':msg}
                
        
        if action == "availability":                                    #prompts user to verify a pending subscription in case lab is full
            if lab_available:
                msg = u"Η υποβολή είναι οριστική, συμβουλευτείτε το πρόγραμμα σας πριν προχωρήσετε"
                data = {'status':1, 'action':action, 'msg':msg}
            else:
                msg = u"To εργαστήριο %s δεν έχει ελεύθερες θέσεις. Θέλετε να υποβάλεται αίτημα στον καθηγητή για την έγκριση της εγγραφή σας?" % lab.classroom.name
                data = {'status':3, 'action':action, 'msg':msg}
        
        if action == "submit":
            try:
                already_subscribed = Subscription.objects.get(student=student, lab__course__lesson__hash_id=lab.course.lesson.hash_id)
                msg = u"Έχετε ήδη εγγραφεί στο συγκεκριμένο μάθημα"
                data = {'status':2, 'action':action, 'msg':msg}
            except:
                subscription = Subscription(student=student, lab=lab)
                
                if lab_available:                                            #subscription completed
                    msg = u"Η εγγραφή σας στο εργαστήριο %s ολοκληρώθηκε" % lab.classroom.name
                else:                                                        #pending subscription completed
                    subscription.in_transit = True
                    msg = u"Στείλαμε το αίτημα σας στον καθηγητή"
                
                try:
                    subscription.save()
                    data = {'status':1, 'action':action, 'msg':msg}
                except ValidationError, e:
                    msg =  e.messages[0]
                    data = {'status':2, 'action':action, 'msg':msg}
        
        if not data:
            error_msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            data = {'status':2, 'msg':error_msg}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/javascript')
        

class SettingsView(AuthenticatedStudentMixin, View):
    
    def get(self, request, username):
        return render(request, 'students/settings.html', {})
        
    def post(self, request, username):
        message = {}
        password = request.POST.get('password','')
        user = request.user
        student = Student.objects.get(user=user)
        
        if password:
            authentication = DionysosAuthentication(username=user.username, password=password, registration_number=student.am, first_name=user.first_name, last_name=user.last_name)
            if authentication.is_valid():
                user.set_password(password)
                user.save()
            else:
                message = {'status':2, 'msg':u'Ο νέος κωδικός δεν αντιστοιχεί σε αυτόν που χρησιμοποιείτε στον Διόνυσο, η αλλαγή ακυρώθηκε'}
        else:
            message = {'status':2, 'msg':u'Ο κωδικός σας δεν μπορεί να είναι κενός'}
        
        if not message:    
            message = {'status':1, 'msg':u'Η αλλαγή κωδικού στον Διογένη ολοκληρώθηκε'}
        context =   {
                    'message':message,
                    }
        return render(request, 'students/settings.html', context)
        

settings = SettingsView.as_view()


@request_passes_test(user_is_student, login_url='/login/')
def has_laptop(request, username):
    ##
    ## message template as above
    ## status 1 green notification, status 2 red notification
    ##
    message = {'status':1, 'msg':u'Οι καθηγητές ενημερώθηκαν για την επιλογή σου'}
    
    context = {
              'message':message,
              }
    return render(request, 'students/settings.html', context)