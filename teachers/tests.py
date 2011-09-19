# -*- coding: utf8 -*-

from diogenis.tests import *

class TeacherTestCase(DiogenisTestCase):
    def test_number_of_schools(self):
        self.assertEqual(self.teacher_2.schools.all().count(), 2)
        
    def test_number_of_teachers_in_informatics_school(self):
        teachers = Teacher.objects.filter(schools__title=u"Πληροφορική")
        self.assertEqual(teachers.count(), 2)
        
    def test_available_teachers_in_informatics_school(self):
        teachers = [self.teacher_1, self.teacher_2]
        for teacher in teachers:
            self.assertTrue(teacher in self.school_1.teacher_set.all())
            
    def test_labs_count(self):
        '''
        Tests Lab.no_conflict()
        '''
        self.assertEqual(Lab.objects.all().count(), 3)
        
    def test_third_student_absences_in_second_teachers_labs(self):
        labs = Lab.objects.filter(teacher=self.teacher_2)
        
        count = 0
        for lab in labs:
            try:
                subscription = Subscription.objects.get(student=self.student_3, lab=lab)
                #print "[%s] %s" % (lab.course.lesson.name, subscription.absences)
                count = count+subscription.absences
            except:
                pass
        self.assertEqual(count, 2)
