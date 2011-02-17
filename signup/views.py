# -*- coding: utf-8 -*-
import os

try:
	from BeautifulSoup import BeautifulSoup
except:
	pass
	
import httplib

try:
	import pycurl
except:
	pass
	
import StringIO
import urllib
import settings
import ldap
import ldap.modlist as modlist


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

def addDataToLDAP(credentials, l):
	attrs = {}
	attrs['objectClass'] = ['person', 'top', 'teilarStudent', 'posixAccount']
	attrs['uid'] =  [credentials['username']]
	attrs['sn'] = [credentials['last_name']]
	attrs['cn'] = [credentials['first_name']]
	attrs['userPassword'] = [credentials['password']]
	attrs['labs'] = credentials['labs']
	try:
		results = l.search_s(settings.SEARCH_DN, ldap.SCOPE_SUBTREE, 'uid=*', ['uidNumber'])
		uids = []
		for item in results:
			uids.append(int(item[1]['uidNumber'][0]))
			attrs['uidNumber'] = [str(max(uids) + 1)]
	except:
 		attrs['uidNumber'] = ['1']
		# ldap is empty, initializing it
		init_attrs1 = {}
		init_attrs1['objectClass'] = ['dcObject', 'organizationalUnit', 'top']
		init_attrs1['dc'] = ['teilar']
		init_attrs1['ou'] = ['TEI Larissas']
		ldif1 = modlist.addModlist(init_attrs1)
		l.add_s('dc=teilar,dc=gr', ldif1)

		init_attrs2 = {}
		init_attrs2['objectClass'] = ['organizationalUnit', 'top']
		init_attrs2['ou'] = ['teilarStudents']
		ldif2 = modlist.addModlist(init_attrs2)
		l.add_s('ou=teilarStudents,dc=teilar,dc=gr', ldif2)

	ldif = modlist.addModlist(attrs)
	l.add_s('uid=%s,ou=teilarStudents,dc=teilar,dc=gr' % (credentials['username']), ldif)
	l.unbind_s()

def signup(request):
	credentials = 0
	msg = 'default'
	if request.method == 'POST':
		form = StudentSignupForm(request.POST)
		if form.is_valid():
			try:
				credentials = checkStudentCredentials(request.POST.get('dionysos_username'), request.POST.get('dionysos_password'))
				if credentials != 0:
					l = ldap.initialize(settings.LDAP_URL)
					l.simple_bind_s(settings.BIND_USER, settings.BIND_PASSWORD)
					try:
						check_user = l.search_s(settings.SEARCH_DN, ldap.SCOPE_SUBTREE, 'uid=%s' % (credentials['username']))
					except:
						addDataToLDAP(credentials, l)
					if check_user:
						msg = "Ο χρήστης υπάρχει ήδη."
						raise
				else:
					msg = "Παρουσιάστηκε σφάλμα στο διόνυσο"
					raise
			except:
				form = ''
				credentials = msg
	else:
		form = StudentSignupForm()
	return render_to_response('signup.html', {
			'form': form,
			'credentials': credentials,
		}, context_instance = RequestContext(request))
