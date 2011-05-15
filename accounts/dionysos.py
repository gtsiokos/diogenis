# -*- coding: utf-8 -*-

import os
import StringIO
import urllib

try:
	from BeautifulSoup import BeautifulSoup
except:
	raise
	
try:
	import pycurl
except:
	raise

def get_student_credentials(username, password):
	'''
	Connects to dionysos.teilar.gr using pycurl, aggregates student's data.
	
	Returns credentials including: 	username | password | last_name | first_name
									registration_number (A.M.) | semester | introduction_year
									labs (current registered labs)
	'''
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
		return {}


