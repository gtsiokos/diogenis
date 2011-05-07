#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from diogenis.labs.models import *

from diogenis.common.helpers import humanize_time
try:
	from reportlab.lib.pagesizes import letter
	from reportlab.lib.styles import getSampleStyleSheet
	from reportlab.lib.units import inch
	from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont
except:
	pass


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
	color = 'black'
	story = []
	studinfo = ''
	lab = Lab.objects.get(name = labtriplet[0], day = labtriplet[1], start_hour = labtriplet[2]['start'], end_hour = labtriplet[2]['end'])
	labInfo = TeacherToLab.objects.get(lab = lab)
	studsub = StudentSubscription.objects.filter(teacher_to_lab = labInfo, in_transit = False).order_by('student').select_related()
	localEdited = u'<font color=%s>%s [%s - %s]</font>' % (color, normalize_locale(labInfo.lesson.name), humanize_time(labInfo.lab.start_hour), humanize_time(labInfo.lab.end_hour))
	story.append(Paragraph(localEdited, style["Heading1"]))
	story.append(Paragraph(normalize_locale(labInfo.teacher.name), style["Heading2"])) 
	localEdited = normalize_locale(labInfo.lab.name)
#	classNum = classNum + 1
	tmp = str('ΕΡΓΑΣΤΗΡΙΟ:')
	tmp = unicode(tmp,"utf-8")
	story.append(Paragraph("<font color='%s'>%s %s</font>" % (color, tmp, localEdited), style["Heading2"]))
	story.append(Paragraph(u" AM  - ΟΝΟΜΑΤΕΠΩΝΥΜΟ ΦΟΙΤΗΤΗ", style["Heading2"]))
	total_subs=len(studsub)
	if total_subs == 0:
		story.append(Spacer(0, inch * .3))
		msg = u"ΔΕΝ ΕΧΟΥΝ ΓΙΝΕΙ ΕΓΓΡΑΦΕΣ ΣΕ ΑΥΤΟ ΤΟ ΕΡΓΑΣΤΗΡΙΟ"
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
