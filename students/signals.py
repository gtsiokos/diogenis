# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

from diogenis.students.models import Subscription

def old_teacher_clear_cache(sender, instance, **kwargs):
    if instance.id is not None:
        subscription = Subscription.objects.get(id=instance.id)
        old_teacher = subscription.lab.teacher
        new_teacher = instance.lab.teacher
        if new_teacher.id is not old_teacher.id:
            old_teacher.clear_cache()
    
def student_teacher_clear_cache(sender, instance, **kwargs):
    instance.student.clear_cache()
    instance.lab.teacher.clear_cache()

pre_save.connect(old_teacher_clear_cache, sender=Subscription, weak=False, dispatch_uid='old_teacher_clear_cache')
post_save.connect(student_teacher_clear_cache, sender=Subscription, weak=False, dispatch_uid='student_teacher_clear_cache')
pre_delete.connect(student_teacher_clear_cache, sender=Subscription, weak=False, dispatch_uid='student_teacher_clear_cache')
