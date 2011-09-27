# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson

from diogenis.students.models import *
from diogenis.teachers.models import *
from diogenis.schools.models import *

from diogenis.common.helpers import humanize_time, set_hour_range
from diogenis.teachers.helpers import get_lab_hour

def user_is_student(user):
    try:
        request_user = Student.objects.get(user=user)
        return user.is_authenticated() and not request_user.is_teacher
    except:
        return False

@user_passes_test(user_is_student, login_url='/login/')
def display_labs(request, username):
    '''
    Manages student's view.
    
    Handling Template:    /students/labs.html
    '''
    if username == request.user.username:
        student = Student.objects.get(user=request.user)
        
        courses = student.get_courses_by_school()
        subscriptions = student.get_subscriptions()
        
        context =   {
                    'subscriptions':subscriptions['context'],
                    'courses':courses['context']
                    }
        return render(request, 'students/labs.html', context)
    else:
        raise Http404


@user_passes_test(user_is_student, login_url="/login/")
def add_new_lab(request):
    '''
    Manages JSON request for lab subscription.
    
    Client-side: [js/core.students.lab.register.js]
    '''
    if request.method == 'POST' and request.is_ajax():
        json_data = simplejson.loads(request.raw_post_data)
        
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
                    hour = get_lab_hour(lab)
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
        
            
