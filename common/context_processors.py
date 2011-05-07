#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

def get_csrf_token_value(request):
	try:
		return { 'csrf_token_value':request.COOKIES['csrftoken'], }
	except:
		return {}

