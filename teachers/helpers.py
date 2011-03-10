#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

import hashlib
from labs.models import *
try:
	from reportlab.lib.pagesizes import letter
	from reportlab.lib.styles import getSampleStyleSheet
	from reportlab.lib.units import inch
	from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont
except:
	pass

def get_hashed_username(username):
	uname_hashed = hashlib.sha256(username)
	return uname_hashed.hexdigest()

def humanize_time(time):
	t = ("%d μ.μ." % (time-12) if time >= 13 else "%d π.μ." % time)
	if time == 12: t = "%d μ.μ." % time
	return t

def get_lab_hour(lab):
	hour = {
			'start':{'raw':lab.start_hour, 'humanized':humanize_time(lab.start_hour)},
			'end':{'raw':lab.end_hour, 'humanized':humanize_time(lab.end_hour)},
			}
	return hour

def set_hour_range(start, end):
	hour = {'start':start, 'end':end}
	return hour

def normalize_locale(text):
	normalizedText = ''
	for achar in text:
		if achar == u'έ':
			achar = u'Ε'
		elif achar == u'ά':
			achar = u'Α'
		elif achar == u'ή':
			achar = u'Η'
		elif achar == u'ί':
			achar = u'Ι'
		elif achar == u'ϊ' or achar == u'Ϊ':
			achar = u"'Ι'"
		elif achar == u'ύ':
			achar = u'Υ'
		elif achar == u'ϋ' or achar == u'Ϋ':
			achar = u"'Υ'"
		elif achar == u'ό':
			achar = u'Ο'
		elif achar == u'ώ':
			achar = u'Ω'

		else:
			achar = achar.capitalize()
		normalizedText = normalizedText + achar
	return normalizedText
	

def pdf_exporter(labtriplet,response):
	localEdited = ''
	pdf = SimpleDocTemplate(response, pagesize = letter)
	style = getSampleStyleSheet()
	color = 'red'
	story = []
	studinfo = ''
	lab = Lab.objects.get(name = labtriplet[0], day = labtriplet[1], hour = labtriplet[2])
	labInfo = TeacherToLab.objects.get(lab = lab)
	studsub = StudentSubscription.objects.filter(teacher_to_lab = labInfo, in_transit = False).order_by('student').select_related()
	title = u'%s - <font color=%s>[ %s ]</font>' % (labInfo.lesson.name, color, labInfo.teacher.name)
	localEdited = normalize_locale(title)
	story.append(Paragraph(localEdited, style["Heading1"]))
	localEdited = normalize_locale(labInfo.lab.name)
#	classNum = classNum + 1
	tmp = str('ΕΡΓΑΣΤΗΡΙΟ:')
	tmp = unicode(tmp,"utf-8")
	story.append(Paragraph("<font color='%s'>%s %s</font>" % (color, tmp, localEdited), style["Heading2"]))
	story.append(Paragraph(u" AM  - ΟΝΟΜΑΤΕΠΩΝΥΜΟ ΦΟΙΤΗΤΗ", style["Heading2"]))
	total_subs=len(studsub)
	if total_subs == 0:
		story.append(Spacer(0, inch * .3))
		msg = "ΔΕΝ ΕΧΟΥΝ ΓΙΝΕΙ ΕΓΓΡΑΦΕΣ ΣΕ ΑΥΤΟ ΤΟ ΕΡΓΑΣΤΗΡΙΟ"
		story.append(Paragraph(msg, style["Normal"]))
		story.append(Spacer(0, inch * .3))
	else:
		for i in range(0,total_subs,1):
			temp = str(studsub[i].student)
			studinfo = unicode(temp,"utf-8")
			studinfo = u'%s - %s' % (studsub[i].student.am, studinfo)
			localEdited = ''
			localEdited = normalize_locale(studinfo)
			story.append(Paragraph(localEdited, style['Normal'],encoding='utf8'))
			story.append(Spacer(0, inch * .1))
	story.append(Spacer(0, inch * .5))
	pdf.build(story)
