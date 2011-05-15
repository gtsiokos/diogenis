#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from diogenis.common.helpers import humanize_time

def get_lab_hour(lab):
	'''
	Expects: Lab object model
	Returns: [Dict] with hour ranges in raw and greek humanized way.
	'''
	hour = {
			'start':{'raw':lab.start_hour, 'humanized':humanize_time(lab.start_hour)},
			'end':{'raw':lab.end_hour, 'humanized':humanize_time(lab.end_hour)},
			}
	return hour
