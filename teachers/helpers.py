#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-

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
    '''
    Normalize locale for pdf exporting
    '''
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
    
def render(template, context):
    from django.template import Context, Template
    t = Template(template)
    c = Context(context)
    return t.render(c)

def pdf_exporter(lab,response):
    from diogenis.teachers.models import Lab
    from diogenis.students.models import Subscription
    #import ipdb; ipdb.set_trace()
    templates = {
                'lab-info': u'<font color="#aaaaaa">{{lesson}} <font color="#555555">[{{start_hour}} - {{end_hour}}]</font> {{classroom}}</font>',
                'student-info': u'<font color="#555555"><font color="#5690C7">{{am}} |</font> {{last_name}} {{first_name}} {% if absences %}<font color="#aaaaaa">/ <strong>{{absences}}</strong></font></font>{% endif %}'
                }
    
    pdf = SimpleDocTemplate(response, pagesize = letter)
    style = getSampleStyleSheet()
    story = []
    
    context =   {
                'lesson':normalize_locale(lab.course.lesson.name),
                'classroom':normalize_locale(lab.classroom.name),
                'start_hour':humanize_time(lab.start_hour),
                'end_hour':humanize_time(lab.end_hour)
                }
    compiled_text = render(templates['lab-info'], context)
    story.append(Paragraph(compiled_text, style["Heading1"]))
    story.append(Spacer(0, inch * .1))
    story.append(Paragraph('<font color="#555555"><font color="#5690C7">Α.Μ. |</font> ΟΝΟΜ/ΠΩΝΥΜΟ ΦΟΙΤΗΤΗ <font color="#aaaaaa">/ ΑΠΟΥΣΙΕΣ</font></font>', style["Heading3"]))
    
    subscriptions = Subscription.objects.filter(lab=lab).order_by('student__user__last_name').select_related()
    pending_subscriptions = subscriptions.filter(in_transit=True)
    subscriptions = subscriptions.filter(in_transit=False)
    story.append(Spacer(0, inch * .2))
    if subscriptions:
        for subscription in subscriptions:
            student = subscription.student
            context =   {
                        'am':student.am,
                        'last_name':normalize_locale(student.user.last_name),
                        'first_name':normalize_locale(student.user.first_name),
                        'absences':subscription.absences
                        }
            compiled_text = render(templates['student-info'], context)
            story.append(Paragraph(compiled_text, style['Normal'],encoding='utf8'))
            story.append(Spacer(0, inch * .1))
    if pending_subscriptions:
        story.append(Spacer(0, inch * .1))
        story.append(Paragraph('<font color="#555555">ΦΟΙΤΗΤΕΣ ΣΤΗΝ ΑΙΘΟΥΣΑ ΑΝΑΜΟΝΗΣ</font>', style["Heading3"]))
        story.append(Spacer(0, inch * .2))
        for subscription in pending_subscriptions:
            student = subscription.student
            context =   {
                        'am':student.am,
                        'last_name':normalize_locale(student.user.last_name),
                        'first_name':normalize_locale(student.user.first_name),
                        }
            compiled_text = render(templates['student-info'], context)
            story.append(Paragraph(compiled_text, style['Normal'],encoding='utf8'))
            story.append(Spacer(0, inch * .1))
    story.append(Spacer(0, inch * .5))
    pdf.build(story)
