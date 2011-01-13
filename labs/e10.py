#!/usr/bin/env python
#coding: UTF-8
#most workable and usefull Ver:2
# -*- coding: utf8 -*-

def fill_labs():
	from labs.models import *
	
	imeres = [u'Δευτέρα',u'Τρίτη',u'Τετάρτη',u'Πέμπτη',u'Παρασκευή']
	onomata_aithouson = [u'ΕΣΕ',u'ΕΡΓ1',u'ΕΡΓ2',u'ΕΡΓ3',u'UNIX',u'NT',u'Τ1',u'Τ2',]
	
	ores_enarksis = []
	for i in range(8,13,2):
		ores_enarksis.append(i)
	i=0
	for i in range(15,20,2):
		ores_enarksis.append(i)

	i=j=k=''
	for i in onomata_aithouson:
		for j in  imeres:
			for k in ores_enarksis:
				tmpobj = Lab(name=i,day=j,hour=k)
				tmpobj.save()


def xls_rdr():
	'''
	Provalei swsta ola ta onomata MONO twn ergastiriakwn kathigitwn kai katw apo kathe omada kathigitwn ena diaxwristiko keno.
	'''
	import re
	import xlrd
	import shutil
	import os,sys
	import settings
	from django.utils.encoding import smart_str, smart_unicode
	
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
	c=0
	
	wb = xlrd.open_workbook(xls_final_pathname)
	sh = wb.sheet_by_index(0)
	
	for rownum in range(sh.nrows):
		b=sh.row_values(rowx=rownum, start_colx=0, end_colx=None)
		for el in b:
			k=smart_str(el)
			i = smart_unicode(k, encoding='utf-8', strings_only=False, errors='strict')
			l=i.find(u'(Ε)')
			if l>0:
				labcells.append(i)
	for j in labcells:
		words=j.split()
		for word in words[2:-1]:
			les=les+' '+word
		lessons.append(les)
		les=''
	
	#for k in lessons:
	#	print k
	for rownum in range(sh.nrows):
		b=sh.row_values(rowx=rownum, start_colx=0, end_colx=None)
		for el in b:
			k=smart_str(el)
			i = smart_unicode(k, encoding='utf-8', strings_only=False, errors='strict')
			l=i.find(u'(Ε)')
			if l>0:
				mess="-------- "+lessons[pos]+" --------"
				pos=pos+1
				temp.append(mess)
				flag2=1
				rownum2=0
				rownum2=rownum+1
				while flag2==1:
					rownum2=rownum2+1
					b2=sh.col_values(1, start_rowx=rownum2, end_rowx=None)
					flag=1						
					for el2 in b2:
						while flag==1:
							k2=smart_str(el2)
							i2=smart_unicode(k2, encoding='utf-8', strings_only=False, errors='strict')
							l2=i2.find(u'ΟΝΟΜΑΤΕΠΩΝΥΜΟ')
							if l2==0:
	#							mess=''
	#							mess="--------"+lessons[pos]+" --------"
	#							pos=pos+1
								flag2=0
	#							temp.append(mess)
							a=str(type(el2).__name__)
							if a=="unicode" and flag2==1:
								temp.append(i2)
								f=f+1
							flag=0
								
			else:
				pass
			
	return temp

