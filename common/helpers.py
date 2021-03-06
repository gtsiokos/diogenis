#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

import hashlib

def get_hashed_id(object_id):
    hashed_id = hashlib.sha256( str(object_id) )
    return hashed_id.hexdigest()

def humanize_time(time):
    t = (u"%d μ.μ." % (time-12) if time >= 13 else u"%d π.μ." % time)
    if time == 12: t = u"%d μ.μ." % time
    return t

