#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

import hashlib

def get_hashed_username(username):
	hashed_username = hashlib.sha256(username)
	return hashed_username.hexdigest()

def humanize_time(time):
	t = (u"%d μ.μ." % (time-12) if time >= 13 else u"%d π.μ." % time)
	if time == 12: t = u"%d μ.μ." % time
	return t

def set_hour_range(start, end):
	hour = {'start':start, 'end':end}
	return hour
