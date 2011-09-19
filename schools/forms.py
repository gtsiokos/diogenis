#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
from random import randrange

from django import forms
from diogenis.schools.models import CoursesUpload
from django.core.exceptions import ValidationError

class CoursesUploadForm(forms.Form):
    file = forms.FileField()
    
    def clean_file(self):
        allowed_content_types = ['application/vnd.ms-excel']
        file = self.cleaned_data['file']
        
        if file.content_type in allowed_content_types:
            data = file
        else:
            raise ValidationError(u"Το αρχείο που ανεβάσατε δεν είναι τύπου excel")
        
        return data

    def save(self, *args, **kwargs):
        school = kwargs.get('school', None)
        if school:
            try:
                courses_upload = CoursesUpload.objects.get(school=school)
                courses_upload.file.delete(save=False)
            except:
                courses_upload = CoursesUpload(school=school)
            
            file = self.cleaned_data['file']
            file.name = u"%s.xls" % school.user.username
            
            courses_upload.file = file
            courses_upload.save()
            
            
