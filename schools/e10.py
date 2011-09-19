#!/usr/bin/env python
# -*- coding: utf-8 -*-
# KWDIKAS ANTIKATASTASHS STO view.py TOU IDIOU labs app.

#28 / 31

from django.utils.encoding import smart_str, smart_unicode
import os
import sys

def xls_rdr(filepath):
	'''
	Provalei swsta ola ta onomata MONO twn ergastiriakwn kathigitwn kai katw apo kathe omada kathigitwn ena diaxwristiko keno.
	'''
	import re
	import xlrd
	import shutil
	
	temp=[]
	lessons=[]
	final=[]
	labcells=[]
	i=''
	j=''
	word=''
	words=[]
	les=''
	pos=0
	flag=0
	flag2=0
	flag3=0
	
	wb = xlrd.open_workbook(filepath)
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
				if a_word.find(e_el) > 0 and a_word[0].isdigit() > 0 and a_word[len(a_word)-1] == e_el:
					labcells.append(a_row)		
	
	for j in labcells:
		words = j.split()
		for word in words[2:]:
			les = les+' '+word
		temp.append(les)
		les = ''

	for rownum in range(sh.nrows):
		all_rows = sh.row_values(rowx=rownum, start_colx=0, end_colx=2)
		for a_row in all_rows:
			a_row = smart_str(a_row)
			a_row = smart_unicode(a_row, encoding='utf-8', strings_only=False, errors='strict')
			lab_creteria = a_row.split()
			for a_word in lab_creteria[1:2]:
				if a_word.find(e_el) > 0 and a_word[0].isdigit() > 0:
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
									flag2 = 0
									#flag3 = 0
								a = str(type(a_col).__name__)
								if a == "unicode" and flag2 == 1 and len(a_col) != 0:
									#print a_col
									flag3 = 1
								flag=0
					if flag3 == 1:
						lessons.append(temp[pos])
						flag3 = 0
					pos = pos + 1
				else:
					pass
	removed_spaces = []
	for i in lessons:
		if i[0] == ' ':
			removed_spaces.append(i[1:])
		else:
			removed_spaces.append(i)
	lessons = removed_spaces
	return lessons
