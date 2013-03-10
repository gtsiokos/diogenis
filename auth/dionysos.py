# -*- coding: utf-8 -*-

#import os
#import StringIO
#import urllib
#import pycurl
from BeautifulSoup import BeautifulSoup
import requests


class DionysosAuthentication(object):
    def __init__(self, *args, **kwargs):
        self.credentials = kwargs
        self.response = self.get_response()
        self.authenticate()
    
    def get_response(self):
        login_post_data = {
            'userName': self.credentials['username'],
            'pwd': self.credentials['password'],
            'submit1': '%C5%DF%F3%EF%E4%EF%F2',
            'loginTrue': 'login'
        }
        
        session = requests.session()
        url = 'https://dionysos.teilar.gr/unistudent/'
        r = session.get(url)
        r = session.post(url, login_post_data)
        r.encoding = 'windows-1253'
        return r.text
    
#    def get_response__legacy(self):
#        curl = pycurl.Curl()
#        stringio = StringIO.StringIO()
#
#        cookie_file_name = os.tempnam('/tmp','dionysos')
#        login_form_seq = [('userName', self.credentials['username']),('pwd', self.credentials['password']),('submit1', '%C5%DF%F3%EF%E4%EF%F2'),('loginTrue', 'login')]
#        login_form_data = urllib.urlencode(login_form_seq)
#        curl.setopt(pycurl.FOLLOWLOCATION, 1)
#        curl.setopt(pycurl.COOKIEFILE, cookie_file_name)
#        curl.setopt(pycurl.COOKIEJAR, cookie_file_name)
#        curl.setopt(pycurl.URL, 'https://dionysos.teilar.gr/unistudent/')
#        curl.setopt(pycurl.POST, 0)
#        curl.perform()
#        curl.setopt(pycurl.URL, 'https://dionysos.teilar.gr/unistudent/login.asp')
#        curl.setopt(pycurl.POST, 1)
#        curl.setopt(pycurl.POSTFIELDS, login_form_data)
#        curl.setopt(pycurl.WRITEFUNCTION, stringio.write)
#        curl.perform()
#        return (stringio.getvalue()).decode('windows-1253')
    
    def authenticate(self):
        self.valid_credentials = {}
        if self.credentials.get('registration_number', ''):
            get_credentials = self._get_credentials
        else:
            get_credentials = self._get_beautifulsoup_credentials
        self.valid_credentials = get_credentials()
        
    def _get_beautifulsoup_credentials(self):
        try:
            credentials = {}
            soup = BeautifulSoup(self.response)
            soup1 = BeautifulSoup(str(soup.findAll('table')[14]))
            soup2 = BeautifulSoup(str(soup1.findAll('tr')[5]))
            credentials['last_name'] = str(soup2.findAll('td')[1].contents[0])
            soup2 = BeautifulSoup(str(soup1.findAll('tr')[6]))
            credentials['first_name'] = str(soup2.findAll('td')[1].contents[0])
            soup2 = BeautifulSoup(str(soup1.findAll('tr')[7]))
            credentials['registration_number'] = str(soup2.findAll('td')[1].contents[0])
            soup2 = BeautifulSoup(str(soup1.findAll('tr')[9]))
            credentials['semester'] = str(soup2.findAll('td')[1].contents[0])
            soup2 = BeautifulSoup(str(soup.findAll('table')[15]))
            season = str(soup2.findAll('span','tablecell')[1].contents[0])[:2]
            if season == 'Ε':
                year = str(soup2.findAll('span','tablecell')[0].contents[0].split('-')[1])
            else:
                year = str(soup2.findAll('span','tablecell')[0].contents[0].split('-')[0])
            credentials['introduction_year'] = year + season
            return dict(self.credentials.items() + credentials.items())
        except Exception, e:
            #print e
            return {}
        
    def _get_credentials(self):
        credentials = self.credentials
        response = self.response
        
        success_count = 0
        for i in 'first_name', 'last_name':
            string_under_test = credentials[i]
            dashed = string_under_test.find("-")
            string_under_test = string_under_test.split()
            splitted = len(string_under_test)
            templist=[]
            full_name_check = 0
            newstring = u""
            a_char = u""
            count = 0
            fullname = u""
            if (splitted > 1) or (dashed > -1):
                for a_word in string_under_test:
                    a_word = a_word + " "
                    for a_char in a_word:
                        if a_char == u"-":
                            newstring = newstring + u" "
                        else:
                            newstring = newstring + a_char
                newstring = newstring.split()

                for a_word in newstring:
                    check = response.find(a_word)
                    if check > -1:
                        full_name_check = full_name_check + 1
                        if count > 0:
                            fullname = fullname + " " + a_word
                        else:
                            fullname = fullname + a_word
                        count = count + 1
                if full_name_check == len(newstring):
                    credentials[i] = fullname
                    success_count = success_count + 1
                else:
                    success_count = success_count - 1
            else:
                if response.find(credentials[i]) > 0:
                    success_count = success_count + 1
                else:
                    success_count = success_count - 1
        if response.find(credentials['registration_number']) > 0:
            success_count = success_count + 1
        else:
            success_count = success_count - 1
        
        credentials = credentials if success_count == 3 else {}
        return credentials
        
    def is_valid(self):
        return True if self.valid_credentials else False

