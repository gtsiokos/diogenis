#!/usr/bin/env python
#coding: UTF-8
# -*- coding: utf8 -*-

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.http import HttpResponse
from labs.models import *

import styles

#u'<font name=times>%s. %s -- %s %s</font>'

def list_reader(username,selected_lesson,response):
	tempname="temp.pdf"
#	response = HttpResponse(mimetype='application/pdf')
#	response['Content-Disposition'] = 'attachment; filename=%s' % (tempname)
#	response['Content-Disposition'] = 'filename=%s' % (tempname)
	pdf = SimpleDocTemplate(response, pagesize = letter)
	
#	fontname = 'Arial'
#	my_location_of_TTF = '/Library/Fonts/Arial.TTF'
#	pdfmetrics.registerFont(TTFont(fontname,my_location_of_TTF))
	style = styles.getSampleStyleSheet()
#	style['Normal'].fontName = fontname
##	style1 = styles.ParagraphStyle({})
##	style1.fontName = fontname
##	arial = pdfmetrics.findFontAndRegister('Arial')	
##	arial.encName = 'ISO-8859-7'
##	stylesheet = {} 
##	ParagraphStyle = styles.ParagraphStyle
##	style = styles.getSampleStyleSheet()
##	style.fontName = fontname
##	style2 = stylesheet
##	style2.fontName = 'Arial'
	
	story = []
	studinfo = ''
#	selected_lesson =str("ΒΑΣΕΙΣ ΔΕΔΟΜΕΝΩΝ ΙΙ")
#	selected_lesson = unicode(selected_lesson,"utf-8")
	username = str(username)
	username =  unicode(username, 'utf8')
	username = Teacher.objects.get(name=username)
	title = u"%s - %s" % (selected_lesson,username)
	story.append(Paragraph(title, style["Heading1"]))
	labs = TeacherToLab.objects.filter(teacher=username).order_by('lesson')
	for a_lab in labs:
		lesson = str(a_lab.lesson)
		lesson = unicode(lesson,'utf8')
		if lesson == selected_lesson:
			labinfo = u"%s - %s - %s" % (a_lab.lab.name,a_lab.lab.day,a_lab.lab.hour)
			story.append(Paragraph(labinfo, style["Heading2"]))
			studsub = StudentSubscription.objects.filter(teacher_to_lab=a_lab, in_transit=False).order_by('student').select_related()
			if len(studsub) == 0:
				story.append(Spacer(0, inch * .3))
				msg = "ΔΕΝ ΕΧΟΥΝ ΓΙΝΕΙ ΕΓΓΡΑΦΕΣ ΣΕ ΑΥΤΟ ΤΟ ΕΡΓΑΣΤΗΡΙΟ"
				story.append(Paragraph(msg, style["Normal"]))
				story.append(Spacer(0, inch * .3))
			else:
				count = 0
				for asub in studsub:
					count = count + 1
					studinfo = str(studinfo)
					#studinfo = unicode(studinfo,"ISO-8859-7")
					studinfo = unicode(studinfo,'utf8')
					studinfo = u'%s. %s -- %s %s' % (count,asub.student.am,asub.student.user.first_name,asub.student.user.last_name)
					story.append(Paragraph(studinfo, style['Normal'],encoding='utf8'))
					story.append(Spacer(0, inch * .1))
		story.append(Spacer(0, inch * .5))
	pdf.build(story)
#	pdf.save()
#	response.write(pdf)
#	return response

