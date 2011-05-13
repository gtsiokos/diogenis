# -*- coding: utf-8 -*-

msg = ''

try:
	from BeautifulSoup import BeautifulSoup
except:
	msg = "Δεν έχει εγκατασταθει το Module της Python: BeautifulSoup"

try:
	import pycurl
except:
	msg = "Δεν έχει εγκατασταθει το Module της Python: pycurl"

import os
import httplib
import StringIO
import urllib
from django.conf import settings


try:
	from diogenis.signup.forms import *
except:
	pass

from django.shortcuts import render_to_response
from django.template import RequestContext

def checkStudentCredentials(username, password):
	conn = pycurl.Curl()
	b = StringIO.StringIO()
	try:
		cookie_file_name = os.tempnam('/tmp','dionysos')
		login_form_seq = [
			('userName', username),
			('pwd', password),
			('submit1', '%C5%DF%F3%EF%E4%EF%F2'),
			('loginTrue', 'login')
		]
		login_form_data = urllib.urlencode(login_form_seq)
		conn.setopt(pycurl.FOLLOWLOCATION, 1)
		conn.setopt(pycurl.COOKIEFILE, cookie_file_name)
		conn.setopt(pycurl.COOKIEJAR, cookie_file_name)
		conn.setopt(pycurl.URL, 'http://dionysos.teilar.gr/unistudent/')
		conn.setopt(pycurl.POST, 0)
		conn.perform()
		conn.setopt(pycurl.URL, 'http://dionysos.teilar.gr/unistudent/login.asp')
		conn.setopt(pycurl.POST, 1)
		conn.setopt(pycurl.POSTFIELDS, login_form_data)
		conn.setopt(pycurl.WRITEFUNCTION, b.write)
		conn.perform()
		soup = BeautifulSoup((b.getvalue()).decode('windows-1253'))

		b1 = StringIO.StringIO()
		conn.setopt(pycurl.URL, 'http://dionysos.teilar.gr/unistudent/stud_NewClass.asp?studPg=1&mnuid=diloseis;newDil&')
		conn.setopt(pycurl.POST, 1)
		conn.setopt(pycurl.POSTFIELDS, login_form_data)
		conn.setopt(pycurl.WRITEFUNCTION, b1.write)
		conn.perform()
		soup_declaration = BeautifulSoup((b1.getvalue()).decode('windows-1253'))

		credentials = {}
		soup1 = BeautifulSoup(str(soup.findAll('table')[14]))
		soup2 = BeautifulSoup(str(soup1.findAll('tr')[5]))
		credentials['last_name'] = str(soup2.findAll('td')[1].contents[0])
		soup2 = BeautifulSoup(str(soup1.findAll('tr')[6]))
		credentials['first_name'] = str(soup2.findAll('td')[1].contents[0])
		soup2 = BeautifulSoup(str(soup1.findAll('tr')[7]))
		credentials['registration_number'] = str(soup2.findAll('td')[1].contents[0])
		soup2 = BeautifulSoup(str(soup1.findAll('tr')[9]))
		credentials['semester'] = str(soup2.findAll('td')[1].contents[0])
#		soup2 = BeautifulSoup(str(soup1.findAll('tr')[8]))
#		credentials['school'] = str(soup2.findAll('td')[1].contents[0]).strip()
		soup2 = BeautifulSoup(str(soup.findAll('table')[15]))
		# introduction year is in type first_year - next_year season
		# if season is 'Εαρινό' we parse the second_year, else the first_year
		season = str(soup2.findAll('span','tablecell')[1].contents[0])[:2]
		if season == 'Ε':
			year = str(soup2.findAll('span','tablecell')[0].contents[0].split('-')[1])
		else:
			year = str(soup2.findAll('span','tablecell')[0].contents[0].split('-')[0])
		credentials['introduction_year'] = year + season
		soup1 = BeautifulSoup(str(soup_declaration.findAll('table')[14]))
		exam_msg = str(soup1.td.contents[0])
		if exam_msg == 'ΝΑ ΜΗΝ ΞΕΧΑΣΩ ΝΑ ΚΑΝΩ ΑΠΟΣΤΟΛΗ ΤΗ ΔΗΛΩΣΗ ΣΤΗ ΓΡΑΜΜΑΤΕΙΑ ΚΑΙ ΝΑ ΕΠΙΒΕΒΑΙΩΣΩ ΤΗΝ ΕΠΙΤΥΧΗ ΑΠΟΣΤΟΛΗ ΤΗΣ !!!':
			soup1 = BeautifulSoup(str(soup_declaration.findAll('table')[16]))
		declaration = []
		k = 8
		tempspan = soup1.findAll('span', 'underline')
		for i in xrange(len(tempspan)):
			lab = str(tempspan[i].contents[0]).strip()
			if lab.endswith('(Ε)'):#(u'\xce\x95')
				declaration.append(lab)
			k += 7
		credentials['labs'] = declaration
		credentials['username'] = username
		credentials['password'] = password
		return credentials
	except:
		return 0

def addDataToAuthDB(credentials):
	user = User(
		username = credentials['username'],
		first_name = credentials['first_name'],
		last_name = credentials['last_name'],
		email = credentials['username'] + '@emptymail.com'
	)
	user.is_staff = False
	user.is_superuser = False
	user.set_password(credentials['password'])
	user.save()

	authStudentProfile = AuthStudent(
		user = user,
		is_teacher = False,
		am = credentials['registration_number'],
		introduction_year = credentials['introduction_year'],
		semester = credentials['semester']
	)	
	authStudentProfile.save()

	if result.has_key('labs'):
		for lab in result['labs']:
			studentLessons = StudentToLesson(
			student = authStudentProfile,
			lesson = Lesson.objects.get(name = lab),
		)
		studentLessons.save()

def signup(request):
	global msg
	if not msg:
		credentials = 0
		if request.method == 'POST':
			form = StudentSignupForm(request.POST)
			if form.is_valid():
				try:
					credentials = checkStudentCredentials(request.POST.get('dionysos_username'), request.POST.get('dionysos_password'))
					if credentials != 0:
						addDataToAuthDB(credentials)
					else:
						msg = "Παρουσιάστηκε σφάλμα στο διόνυσο"
						raise
				except:
					form = ''
					credentials = msg
		else:
			form = StudentSignupForm()
	else:
		form = ''
		credentials = msg
	return render_to_response('signup.html', {
			'form': form,
			'credentials': credentials,
		}, context_instance = RequestContext(request))

