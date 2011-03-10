#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

from diogenis.labs.models import *

def fill_labs():
	days = [u'Δευτέρα',u'Τρίτη',u'Τετάρτη',u'Πέμπτη',u'Παρασκευή']
	classrooms = Classroom.objects.all()
	
	i=j=''
	for classroom in classrooms:
		for day in days:
			lab = Lab(name=classroom.name, day=day, start_hour=1, end_hour=1)
			lab.save()


def xls_rdr():
	'''
	Provalei swsta ola ta onomata MONO twn ergastiriakwn kathigitwn kai katw apo kathe omada kathigitwn ena diaxwristiko keno.
	'''
	
	import re
	import xlrd
	import shutil
	import os,sys
	from django.utils.encoding import smart_str, smart_unicode
	import settings
	
	xls_final_pathname = '%s/ANATHESEIS.xls' % (settings.MEDIA_ROOT)
	teachers=[]
	labcells=[]
	lessons=[]
	temp=[]
	i=''
	word=''
	words=[]
	les=''
	j=''
	f=0
	l=0
	l2=0
	isit=''
	flag=1
	flag2=1
	mess=''
	pos=0
	
	wb = xlrd.open_workbook(xls_final_pathname)
	sh = wb.sheet_by_index(0)
	
	e_el = u'Ε'
	e_el = smart_str(e_el)
	e_el = smart_unicode(e_el, encoding='utf-8', strings_only=False, errors='strict')
	
	for rownum in range(sh.nrows):
		all_rows=sh.row_values(rowx=rownum, start_colx=0, end_colx=1)
		for a_row in all_rows:
			a_row = smart_str(a_row)
			a_row = smart_unicode(a_row, encoding='utf-8', strings_only=False, errors='strict')
			lab_creteria = a_row.split()
			for a_word in lab_creteria[1:2]:
				if a_word.find(e_el) > 0 and a_word[0].isdigit() > 0:
					labcells.append(a_row)		
	
	for j in labcells:
		words = j.split()
		for word in words[2:]:
			les = les+' '+word
		lessons.append(les)
		les = ''
	
	#for k in lessons:
	#	print k
	for rownum in range(sh.nrows):
		all_rows = sh.row_values(rowx=rownum, start_colx=0, end_colx=2)
		for a_row in all_rows:
			a_row = smart_str(a_row)
			a_row = smart_unicode(a_row, encoding='utf-8', strings_only=False, errors='strict')
			lab_creteria = a_row.split()
			for a_word in lab_creteria[1:2]:
				if a_word.find(e_el) > 0 and a_word[0].isdigit() > 0:
					mess = "-------- "+lessons[pos]+" --------"
					pos = pos + 1
					temp.append(mess)
					flag2 = 1
					rownum2 = 0
					rownum2 = rownum+1
					while flag2 == 1:
						rownum2=rownum2+1
						all_col=sh.col_values(1, start_rowx=rownum2, end_rowx=None)
						flag = 1						
						for a_col in all_col:
							while flag == 1:
								a_col = smart_str(a_col)
								a_col = smart_unicode(a_col, encoding='utf-8', strings_only=False, errors='strict')
								check_list = a_col.find(u'ΟΝΟΜΑΤΕΠΩΝΥΜΟ')
								if check_list == 0:
		#							mess=''
		#							mess="--------"+lessons[pos]+" --------"
		#							pos=pos+1
									flag2 = 0
		#							temp.append(mess)
								a = str(type(a_col).__name__)
								if a == "unicode" and flag2 == 1:
									temp.append(a_col)
									f = f + 1
								flag=0
								
				else:
					pass
	return temp
