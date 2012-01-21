#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from django.core.cache import cache

from diogenis.settings import REDIS as r
from diogenis.auth.models import UserProfile
from diogenis.schools.models import Course
from diogenis.students.models import Subscription

from diogenis.common.helpers import get_hashed_id, humanize_time


class Teacher(UserProfile):
    '''
    Extends UserProfile model for teachers.
    '''
    schools = models.ManyToManyField('schools.School')
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = u"Καθηγητής"
        verbose_name_plural = u"Καθηγητές"
    
    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)
    
    def save(self, *args, **kwargs):
        self.is_teacher = True
        super(Teacher, self).save(*args, **kwargs)
        if not self.hash_id:
            self.hash_id = get_hashed_id(self.user.id)
            super(Teacher, self).save(*args, **kwargs)
    
    def clear_cache(self):
        username = self.user.username
        keys = r.keys(u'*teachers/%s*' % username)
        for key in keys:
            r.delete(key)
        return None
    
    def get_courses_by_school(self):
        context = []
        schools = self.schools.all().order_by('title').select_related()
        for school in schools:
            labs = Lab.objects.filter(teacher=self, course__school=school).order_by('course__lesson__name').select_related()
            lessons_ids = labs.values_list('course__lesson__id', flat=True)
            courses = Course.objects.filter(school=school, lesson__id__in=lessons_ids).order_by('lesson__name').select_related()
            item =  {
                    'school':school.title,
                    'lessons':courses.values('hash_id', 'lesson__name')
                    }
            context.append(item)
        
        return {'objects':courses, 'context':context}
    
    def json(self, selected_school=None):
        
        json =  {
                'id': self.hash_id,
                'firstname': self.user.first_name,
                'lastname': self.user.last_name,
                'username': self.user.username,
                'schools': [school.json() for school in self.schools.all()]
                }
        
        if selected_school:
            courses_list = Lab.objects.filter(teacher=self, course__school=selected_school).values_list('course__hash_id', flat=True)
            school_courses = Course.objects.filter(school=selected_school).select_related('school__title', 'lesson__name')
            
            courses = []
            for course in school_courses:
                if course.hash_id in courses_list:
                    course = course.json()
                    course['selected'] = True
                    courses.append(course)
                else:
                    courses.append(course.json())
            
            json['courses'] = courses
        
        return json


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = u"Αίθουσα"
        verbose_name_plural = u"Αίθουσες"
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        super(Classroom, self).save(*args, **kwargs)
        if not self.hash_id:
            self.hash_id = get_hashed_id(self.id)
            super(Classroom, self).save(*args, **kwargs)

    def json(self):
        return  {
                'id': self.hash_id,
                'name': self.name,
                }
 
class Lab(models.Model):
    classroom = models.ForeignKey('Classroom', blank=True, null=True)
    teacher = models.ForeignKey('Teacher')
    course = models.ForeignKey('schools.Course', blank=True, null=True)
    
    day = models.CharField(max_length=10, blank=True, null=True)
    start_hour = models.IntegerField(default=1, max_length=2)
    end_hour = models.IntegerField(default=2, max_length=2)
    max_students = models.IntegerField(max_length=2, null=True, blank=True)
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = u"Εργαστήριο"
        verbose_name_plural = u"Εργαστήρια"
        ordering = ['course']
    
    def __unicode__(self):
        to_string = u'%s | %s - %s' % (self.course.school.title, self.course.lesson.name, self.teacher.user.get_full_name())
        try:
            to_string += u' [ %s - %s (%s - %s) ]' % (self.classroom.name, self.day, self.start_hour, self.end_hour)
        except:
            pass
        return to_string
    
    def save(self, *args, **kwargs):
        conflict = False if self.start_hour==1 else not self.check_conflict()
        if self.id is not None and self.start_hour < self.end_hour:
            super(Lab, self).save(*args, **kwargs)    
        else:   #Initial save()
            if conflict:
                raise ValidationError(u"Η αίθουσα δεν είναι διαθέσιμη")
            elif self.start_hour >= self.end_hour:
                raise ValidationError(u"H ώρα έναρξης του εργαστηρίου είναι μεγαλύτερη της ώρας λήξης")
            super(Lab, self).save(*args, **kwargs)    
            if not self.hash_id:
                self.hash_id = get_hashed_id(self.id)
                super(Lab, self).save(*args, **kwargs)
    
    def check_conflict(self, *args, **kwargs):
        '''
        Checks hour conflict with already created labs.
        
        Arguments:    [new_lab]
        Returns:     True | False
        '''
        start = self.start_hour
        end = self.end_hour
        
        labs = Lab.objects.filter(day__contains=self.day, classroom__name__contains=self.classroom.name, start_hour__gt=1)
        #print labs
        flag = -1
        if labs:
            for lab in labs:
                if (( (start > lab.end_hour) or (start == lab.end_hour) ) or ( (end == lab.start_hour) or (end < lab.start_hour) )):
                    a = 2
                else:
                    flag = 0
        
        return False if flag==0 else True
    
    @property
    def hour(self):
        '''
        Returns: [Dict] with hour ranges in raw and greek humanized way.
        '''
        hour = {
                'start':{'raw':self.start_hour, 'humanized':humanize_time(self.start_hour)},
                'end':{'raw':self.end_hour, 'humanized':humanize_time(self.end_hour)},
                }
        return hour
        
    @hour.setter
    def hour(self, hour):
        self.start_hour = hour.get('start', 1)
        self.end_hour = hour.get('end', 1)
    
    @property
    def registered_students_count(self):
        subscriptions = Subscription.objects.filter(lab=self)
        return len(subscriptions)
    
    @property
    def empty_seats(self):
        registered_students_count = self.registered_students_count
        return ( self.max_students-registered_students_count if self.max_students>registered_students_count else 0 )
    
    @property
    def sibling_labs_plus_self(self):
        all_labs = Lab.objects.filter(course=self.course, start_hour__gt=1).order_by('start_hour').select_related('classroom__name')
        owners_labs = all_labs.filter(teacher=self.teacher)
        owners_labs_ids = owners_labs.values_list('id', flat=True)
        others_labs = all_labs.exclude(id__in=owners_labs_ids)
        return {'owners':owners_labs, 'others':others_labs}
    
    @property
    def sibling_labs(self):
        labs = self.sibling_labs_plus_self
        labs['owners'] = labs['owners'].exclude(id=self.id)
        return labs

import diogenis.teachers.signals
