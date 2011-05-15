#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

def get_csrf_token_value(request):
    '''
    Custom context processor, creates a {{csrf_token_value}} template tag for logged-in users.
    
    Current use: diogenis.teachers.views -> pdf_export [checks valid csrf_token]
    '''
    try:
        return { 'csrf_token_value':request.COOKIES['csrftoken'], }
    except:
        return {}

