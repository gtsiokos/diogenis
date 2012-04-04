#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8

from django.db import models, transaction

from diogenis.auth.models import UserProfile

from diogenis.common.helpers import get_hashed_id
from diogenis.schools.e10 import xls_rdr as get_lessons


class School(UserProfile):
    '''
    Extends UserProfile model for secretary of each school.
    '''
    title = models.CharField(max_length=333)
    lessons = models.ManyToManyField('Lesson', through='Course', null=True, blank=True)
    classrooms = models.ManyToManyField('teachers.Classroom', null=True, blank=True)
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
        
    class Meta:
        ordering = ['title']
        verbose_name = u"Τμήμα"
        verbose_name_plural = u"Τμήματα"
    
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        self.is_school = True
        super(School, self).save(*args, **kwargs)
        if not self.hash_id:
            self.hash_id = get_hashed_id(self.user.id)
            super(School, self).save(*args, **kwargs)
    
    def json(self):
        return  {
                'id':self.hash_id,
                'title':self.title
                }

class Lesson(models.Model):
    name = models.CharField(max_length=333)
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = u"Μάθημα"
        verbose_name_plural = u"Μαθήματα"
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        super(Lesson, self).save(*args, **kwargs)
        if not self.hash_id:
            self.hash_id = get_hashed_id(self.id)
            super(Lesson, self).save(*args, **kwargs)
        
class Course(models.Model):
    school = models.ForeignKey('School')
    lesson = models.ForeignKey('Lesson')
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['school', 'lesson']
        verbose_name = u"Μάθημα ανά Τμήμα"
        verbose_name_plural = u"Μαθήματα ανά Τμήμα"
        
    def __unicode__(self):
        return u'%s | %s' % (self.school.title, self.lesson.name)
        
    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)
        if not self.hash_id:
            self.hash_id = get_hashed_id(self.id)
            super(Course, self).save(*args, **kwargs)
            
    def json(self):
        return  {
                'id': self.hash_id,
                'school': self.school.title,
                'lesson': self.lesson.name
                }
                
class CoursesUpload(models.Model):
    school = models.OneToOneField('School', unique=True)
    file = models.FileField(upload_to='uploads/courses/', blank=True, null=True)
    
    class Meta:
        ordering = ['school']
        verbose_name = u"Ανεβασμένο Πρόγραμμα Σπουδών"
        verbose_name_plural = u"Ανεβασμένα Προγράμματα Σπουδών"
    
    def __unicode__(self):
        return u'%s' % self.school.title
    
    def save(self, *args, **kwargs):
        from diogenis.students.models import Student
        from diogenis.teachers.models import Teacher
        
        super(CoursesUpload, self).save(*args, **kwargs)
        lessons_list = get_lessons(self.file.path)
        #import ipdb; ipdb.set_trace();
        lessons = self.school.lessons.all()
        lessons.delete()
        
        for lesson_name in lessons_list:
            lesson = Lesson(name=lesson_name)
            lesson.save()
            course = Course(lesson=lesson, school=self.school)
            course.save()
        
        students = Student.objects.filter(schools__in=[self.school])
        [student.clear_cache() for student in students]
        teachers = Teacher.objects.filter(schools__in=[self.school])
        [teacher.clear_cache() for teacher in teachers]
            
    def delete(self, *args, **kwargs):
        try:
            self.file.delete()
            
            students = Student.objects.filter(schools__in=[self.school])
            [student.clear_cache() for student in students]
        except:
            pass
        super(CoursesUpload, self).delete(*args, **kwargs)
