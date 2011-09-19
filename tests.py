# -*- coding: utf8 -*-

from django.test import TestCase

from django.core.exceptions import *

from django.contrib.auth.models import User
from diogenis.auth.models import UserProfile
from diogenis.teachers.models import Teacher, Lab, Classroom
from diogenis.students.models import Student, Subscription
from diogenis.schools.models import School, Course, Lesson

class DiogenisTestCase(TestCase):
    
    def setUp(self):
        #Models without Relations
        self.populate_school_users()
        self.populate_teacher_users()
        self.populate_student_users()
        self.populate_lessons()
        self.populate_classrooms()
        
        #Models with Relations
        self.populate_userprofiles()
        self.populate_courses()
        self.populate_labs()
        self.populate_subscriptions()
        
    def populate_school_users(self):
        self.school_1 = User(username='informatics')
        self.school_1.set_password('1')
        self.school_1.save()
        
        self.school_2 = User(username='logistics')
        self.school_2.set_password('1')
        self.school_2.save()
        
        return self
        
    def populate_teacher_users(self):
        self.teacher_1 = User(username='gkarani', first_name=u"ΓΕΩΡΓΙΑ", last_name=u"ΓΚΑΡΑΝΗ")
        self.teacher_1.set_password('1')
        self.teacher_1.save()
        
        self.teacher_2 = User(username='mpezos', first_name=u"ΝΙΚΟΣ", last_name=u"ΜΠΕΖΟΣ")
        self.teacher_2.set_password('1')
        self.teacher_2.save()
        
        return self
        
    def populate_student_users(self):
        self.student_1 = User(username='fusion', first_name=u"ΓΙΩΡΓΟΣ", last_name=u"ΤΣΙΩΚΟΣ")
        self.student_1.set_password('1')
        self.student_1.save()
        
        self.student_2 = User(username='lomar', first_name=u"ΣΤΕΦΑΝΟΣ", last_name=u"ΧΡΟΥΣΗΣ")
        self.student_2.set_password('1')
        self.student_2.save()
        
        self.student_3 = User(username='notisx', first_name=u"ΧΡΗΣΤΟΣ", last_name=u"ΝΟΤΗΣ")
        self.student_3.set_password('1')
        self.student_3.save()
        
        self.student_4 = User(username='tsolis', first_name=u"ΔΗΜΗΤΡΗΣ", last_name=u"ΤΣΟΛΗΣ")
        self.student_4.set_password('1')
        self.student_4.save()
        
        self.student_5 = User(username='natsios', first_name=u"ΧΡΗΣΤΟΣ", last_name=u"ΝΑΤΣΙΟΣ")
        self.student_5.set_password('1')
        self.student_5.save()
        
        return self
        
    def populate_userprofiles(self):
        self.school_1 = School(user=self.school_1, title=u"Πληροφορική")
        self.school_1.save()
        
        self.school_2 = School(user=self.school_2, title=u"Λογιστική")
        self.school_2.save()
        
        self.student_1 = Student(user=self.student_1, am='1111', introduction_year=u"2006X", semester='10')
        self.student_1.save()
        self.student_1.schools.add(self.school_1)
        
        self.student_2 = Student(user=self.student_2, am='2222', introduction_year=u"2007X", semester='9')
        self.student_2.save()
        self.student_2.schools.add(self.school_1)
        
        self.student_3 = Student(user=self.student_3, am='3333', introduction_year=u"2008X", semester='8')
        self.student_3.save()
        self.student_3.schools.add(self.school_1)
        self.student_3.schools.add(self.school_2)
        
        self.student_4 = Student(user=self.student_4, am='4444', introduction_year=u"2008X", semester='8')
        self.student_4.save()
        self.student_4.schools.add(self.school_2)
        
        self.student_5 = Student(user=self.student_5, am='5555', introduction_year=u"2006X", semester='8')
        self.student_5.save()
        self.student_5.schools.add(self.school_1)
        self.student_5.schools.add(self.school_2)
        
        self.teacher_1 = Teacher(user=self.teacher_1)
        self.teacher_1.save()
        self.teacher_1.schools.add(self.school_1)
        
        self.teacher_2 = Teacher(user=self.teacher_2)
        self.teacher_2.save()
        self.teacher_2.schools.add(self.school_1)
        self.teacher_2.schools.add(self.school_2)
        
        return self
        
    def populate_lessons(self):
        self.lesson_1 = Lesson(name=u"Προγραμματισμός 1")
        self.lesson_1.save()
        
        self.lesson_2 = Lesson(name=u"Εισαγωγή στο Excel")
        self.lesson_2.save()
        
        return self
        
    def populate_courses(self):
        self.course_1 = Course(school=self.school_1, lesson=self.lesson_1)
        self.course_1.save()
        
        self.course_2 = Course(school=self.school_1, lesson=self.lesson_2)
        self.course_2.save()
        
        self.course_3 = Course(school=self.school_2, lesson=self.lesson_2)
        self.course_3.save()
        
        return self
    
    def populate_classrooms(self):
        self.classroom_1 = Classroom(name=u"UNIX")
        self.classroom_1.save()
        
        self.classroom_2 = Classroom(name=u"NT")
        self.classroom_2.save()
        
        self.classroom_3 = Classroom(name=u"ΔΙΑΛ 1")
        self.classroom_3.save()
        
        self.classroom_4 = Classroom(name=u"ΔΙΑΛ 2")
        self.classroom_4.save()        
        
        return self
        
    def populate_labs(self):
        self.lab_1 = Lab(classroom=self.classroom_1,teacher=self.teacher_1,course=self.course_1,day=u"Δευτέρα",start_hour=12, end_hour=14, max_students=14)
        self.lab_1.save()
        
        self.lab_2 = Lab(classroom=self.classroom_3,teacher=self.teacher_2,course=self.course_2,day=u"Δευτέρα",start_hour=10, end_hour=13, max_students=14)
        self.lab_2.save()
        
        self.lab_3 = Lab(classroom=self.classroom_4,teacher=self.teacher_2,course=self.course_3,day=u"Τρίτη",start_hour=10, end_hour=13, max_students=14)
        self.lab_3.save()
        
        try:
            self.lab_4 = Lab(classroom=self.classroom_4,teacher=self.teacher_2,course=self.course_3,day=u"Τρίτη",start_hour=9, end_hour=12, max_students=14)
            self.lab_4.save()
        except Exception, e:
            if(type(e).__name__ == 'ValidationError'):
                pass
                #import traceback, os.path
                #top = traceback.extract_stack()[-1]
                #print ", ".join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
        
        return self
        
    def populate_subscriptions(self):
        self.subscription_1 = Subscription(student=self.student_1 , lab=self.lab_1 )
        self.subscription_2 = Subscription(student=self.student_2 , lab=self.lab_1 )
        self.subscription_3 = Subscription(student=self.student_3 , lab=self.lab_2, absences=2 )
        self.subscription_4 = Subscription(student=self.student_4 , lab=self.lab_3 )
        self.subscription_5 = Subscription(student=self.student_5 , lab=self.lab_2 )
        
        
        self.subscription_1.save()
        self.subscription_2.save()
        self.subscription_3.save()
        self.subscription_4.save()
        self.subscription_5.save()
        
        try:
            self.subscription_6 = Subscription(student=self.student_3 , lab=self.lab_1)
            self.subscription_6.save()
        except Exception, e:
            if(type(e).__name__ == 'ValidationError'):
                pass
        
        return self
    
