# -*- coding: utf8 -*-

from diogenis.tests import *

class StudentTestCase(DiogenisTestCase):
    def test_subscriptions_count(self):
        '''
        Tests Subscription.check_availability()
        '''
        self.assertEqual(Subscription.objects.all().count(), 6)
        
    def test_lessons_by_student(self):
        students = Student.objects.all()
        for student in students:
            subscriptions = Subscription.objects.filter(student=student)
            if student.am == '1111':
                self.assertEqual(subscriptions.count(), 1)
            if student.am == '2222':
                self.assertEqual(subscriptions.count(), 1)
            if student.am == '3333':
                self.assertEqual(subscriptions.count(), 2)
