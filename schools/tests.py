# -*- coding: utf8 -*-

from diogenis.tests import *

class SchoolTestCase(DiogenisTestCase):
    def test_lessons_count_for_informatics(self):
        self.assertEqual(self.school_1.lessons.all().count(), 2)
        
    def test_schools_count_for_second_lesson(self):
        self.assertEqual(self.lesson_2.school_set.all().count(), 2)
        
    
