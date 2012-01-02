#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

from diogenis.teachers.models import Teacher, Lab

def teacher_clear_cache(sender, instance, **kwargs):
    instance.teacher.clear_cache()

def affiliate_teachers_clear_cache(sender, instance, **kwargs):
    course_id = instance.course.id
    teachers_id = Lab.objects.filter(course__id=course_id).values_list('teacher__id', flat=True)
    teachers = Teacher.objects.filter(id__in=teachers_id)
    [teacher.clear_cache() for teacher in teachers]

post_save.connect(teacher_clear_cache, sender=Lab, weak=False, dispatch_uid='teacher_clear_cache')
pre_delete.connect(teacher_clear_cache, sender=Lab, weak=False, dispatch_uid='teacher_clear_cache')
pre_delete.connect(affiliate_teachers_clear_cache, sender=Lab, weak=False, dispatch_uid='affiliate_teachers_clear_cache')
