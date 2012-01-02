# -*- coding: utf-8 -*-

messages = []

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import auth
from django.utils import simplejson

from django.contrib.auth.models import User
from diogenis.teachers.models import Teacher
from diogenis.students.models import Student, Subscription
from diogenis.schools.models import School

from diogenis.auth.forms import StudentSignupForm
from diogenis.auth.dionysos import DionysosAuthentication


def login(request):
    '''
    Authenticates username and password, creates a session and redirects user to the respective page.
    '''
    if request.method == "POST":
        post = request.POST.copy()
        #import ipdb; ipdb.set_trace();
        if post.has_key('username') and post.has_key('password') or post.has_key('login-username') and post.has_key('login-password'):
            try:
                usr = post['username']
                pwd = post['password']
            except:
                usr = post['login-username']
                pwd = post['login-password']
            remember = False
            if post.has_key('remember'):
                remember = True
            user = auth.authenticate(username=usr, password=pwd)
            if user is not None and not user.is_superuser:
                auth.login(request, user)
                if remember==False:
                    request.session.set_expiry(0)
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
                return render(request, 'index.html', {'message':u'Ο λογαριασμός δεν υπάρχει'})
            
    return render(request, 'authentication/login.html', {})


def logout(request):
    '''
    Logs out user
    '''
    auth.logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    '''
    Signup form for students.
    
    Uses DionysosAuthentication for retrieving student's data from dionysos.teilar.gr
    '''
    if request.method == 'POST' and request.is_ajax():
        json_data = simplejson.loads(request.raw_post_data)
        data = {}
        
        try:
            action = json_data['action']
        except KeyError:
            msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            data = {'status':2, 'msg':msg}
        
        if action == 'authenticate':
            try:
                username = json_data['username']
                password = json_data['password']
                registration_number = json_data.get('registration-number', '')
                first_name = json_data.get('first-name', '')
                last_name = json_data.get('last-name', '')
            except KeyError:
                msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
                data = {'status':2, 'msg':msg}
            
            form = StudentSignupForm({'username':username,'password':password})
            if form.is_valid():
                if registration_number:
                    authentication = DionysosAuthentication(username=username, password=password, registration_number=registration_number, first_name=first_name, last_name=last_name)
                else:
                    authentication = DionysosAuthentication(username=username, password=password)
                if authentication.is_valid():
                    credentials = authentication.valid_credentials
                    try:
                        user = User.objects.get(username=credentials['username'])
                    except:
                        user = User(
                            username = credentials['username'],
                            first_name = credentials['first_name'],
                            last_name = credentials['last_name'],
                            email = credentials['username'] + '@emptymail.com'
                        )
                        user.set_password(credentials['password'])
                        user.save()
                        
                    schools = School.objects.order_by('title')
                    schools = map(school_info, schools)
                    data = {'status':1, 'action':action, 'credentials':credentials, 'schools':schools}
                else:
                    msg = u"Λάθος στοιχεία, θυμηθείτε αν αλλάξατε τον κωδικό σας"
                    data = {'action':action, 'status':2, 'msg':msg}
            else:
                msg = u"Συμπληρώστε σωστά τα στοιχεία σας"
                data = {'action':action, 'status':2, 'msg':msg}
        
        if action == 'signup':
            #import ipdb; ipdb.set_trace();
            try:
                student = json_data['student']
                school_id = json_data['school_id']
            except KeyError:
                msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
                data = {'status':2, 'msg':msg}
            
            school = School.objects.get(hash_id=school_id)
            user = User.objects.get(username=student['username'], last_name=student['last_name'], first_name=student['first_name'])
            try:
                student = Student(
                    user = user,
                    am = student['registration_number'],
                    introduction_year = student['introduction_year'],
                    semester = student['semester']
                )
                student.save()
                student.schools.add(school)
                student.save()
                
                subscriptions = Subscription.objects.filter(student=student)
                subscriptions.delete()
                
                if student.user is not None and student.user.is_active:
                    msg = u"H εγγραφή ολοκληρώθηκε, μπορείτε να κάνετε login με τα στοιχεία σας από τον Διόνυσο"
                    data = {"status": 1, "msg": msg}
            except IntegrityError:
                msg = u"Έχετε κάνει ήδη εγγραφή, δοκιμάστε να κάνετε login"
                data = {"status": 1, "msg": msg}
                    
        if not data:
            error_msg = u"Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων"
            data = {'status':2, 'msg':error_msg}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/javascript')
    else:
        context = {}
        return render(request, 'authentication/signup.html', context)


def school_info(school):
    return {'title':school.title, 'id':school.hash_id}


