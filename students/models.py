#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.db import models
from django.core.exceptions import ValidationError
from django.core.cache import cache

from diogenis.settings import REDIS as r
from diogenis.auth.models import UserProfile
from diogenis.schools.models import Course

from diogenis.common.helpers import get_hashed_id

class Student(UserProfile):
    '''
    Extends UserProfile model for students.
    
    [am] field is the registration id for every student. 
    '''
    am = models.CharField(max_length=15)
    introduction_year = models.CharField(max_length = 15)
    semester = models.CharField(max_length = 2)
    schools = models.ManyToManyField('schools.School')
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['am']
        verbose_name = u"Φοιτητής"
        verbose_name_plural = u"Φοιτητές"
    
    def __unicode__(self):
        return u'[%s] %s %s' % (self.am, self.user.last_name, self.user.first_name)
    
    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)
        if not self.hash_id:
            self.hash_id = get_hashed_id(self.user.id)
            super(Student, self).save(*args, **kwargs)
    
    def clear_cache(self):
        username = self.user.username
        keys = r.keys(u'*students/%s*' % username)
        for key in keys:
            r.delete(key)
        return None
    
    def get_courses_by_school(self):
        context = []
        schools = self.schools.all().order_by('title').select_related()
        for school in schools:
            courses = Course.objects.filter(school=school).order_by('lesson__name').select_related()
            if courses:
                item = {
                       'school':school.title,
                       'lessons':courses.values('hash_id', 'lesson__name')
                       }
                context.append(item)
        
        return {'objects':courses, 'context':context}
    
    def _map_subscriptions(self, subscription):
        return  {
                'lesson':subscription.lab.course.lesson.name,
                'classroom':subscription.lab.classroom.name,
                'day':subscription.lab.day,
                'hour':subscription.lab.hour,
                'absences':subscription.opinionated_absences,
                'teacher':subscription.lab.teacher.user.get_full_name(),
                }
    
    def get_subscriptions(self):
        context = []
        subscriptions = Subscription.objects.filter(student=self).select_related('lab__course__lesson__name', 'lab__classroom__name', 'lab__teacher__user')
        
        verified = subscriptions.filter(in_transit=False)
        verified = map(self._map_subscriptions, verified)
        
        in_transit = subscriptions.filter(in_transit=True)
        in_transit = map(self._map_subscriptions, in_transit)
        
        context = {'verified':verified, 'in_transit':in_transit}
        return {'context':context}


class Subscription(models.Model):
    student = models.ForeignKey('Student')
    lab = models.ForeignKey('teachers.Lab')    
    course = models.ForeignKey('schools.Course', blank=True, null=True)
    
    in_transit = models.BooleanField(default=False)
    absences = models.IntegerField(default=0, max_length=2)
    hash_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['student']
        verbose_name = u"Εγγραφή"
        verbose_name_plural = u"Εγγραφές"
    
    def __unicode__(self):
        return u'[%s] %s - %s' % (self.student.am, self.student.user.get_full_name(), self.lab.course.lesson.name)
    
    def save(self, *args, **kwargs):
        self.check_valid_school()
        available = self.check_availability()
        if self.id is not None:
            if not available:   #In case you try to change registered lab from django admin
                raise ValidationError(u"Κάποιοι σπουδαστές έχουν δηλώσει άλλα εργαστήρια αυτές τις ώρες")
            if self.absences < 0:
                self.absences = 0
            super(Subscription, self).save(*args, **kwargs)
        else:   #Initial save()
            if not available:
                raise ValidationError(u"Έχετε δηλώσει άλλο εργαστήριο αυτές τις ώρες, δοκιμάστε άλλη ώρα ή επιλέξτε άλλον καθηγητή")
            super(Subscription, self).save(*args, **kwargs)
            if not self.hash_id:
                self.hash_id = get_hashed_id(self.id)
                self.course = self.lab.course
                super(Subscription, self).save(*args, **kwargs)
    
    def check_valid_school(self, *args, **kwargs):
        if self.lab.course.school not in self.student.schools.all():
            raise ValidationError(u"O φοιτητής δεν ανοίκει στην συγκεκριμένη σχολή")
    
    def check_availability(self, *args, **kwargs):
        '''
        Checks student's availability in order to be transferred.
        
        Arguments:    [new_lab] - Teacher's lab to be tranferred
                    [student]
        
        Returns:    True | False
        '''
        student = self.student
        day = self.lab.day
        start = self.lab.start_hour
        end = self.lab.end_hour
        subscriptions = Subscription.objects.filter(student=student, lab__day__contains=day).exclude(id=self.id).select_related()
        #import ipdb; ipdb.set_trace();
        flag = -1
        if subscriptions:
            for subscription in subscriptions:
                lab = subscription.lab
                if (( (start > lab.end_hour) or (start == lab.end_hour) ) or ( (end == lab.start_hour) or (end < lab.start_hour) )):
                    a = 2
                else:
                    flag = 0
        
        return False if flag==0 else True
    
    @property
    def opinionated_absences(self):
        absences = self.absences
        result = {}
        result['value'] = self.absences
        result['subscription_id'] = self.hash_id
        
        if absences>1:
            result['importance'] = 'warning'
        else:
            result['importance'] = ''
        return result

import diogenis.students.signals
