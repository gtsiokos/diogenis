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

class DionysosAuthentication(object):
    def __init__(self, *args, **kwargs):
        #import ipdb; ipdb.set_trace();
        self.credentials = kwargs
        self.response = self.get_response()
        self.authenticate()
    
    def get_response(self):
        curl = pycurl.Curl()
        stringio = StringIO.StringIO()

        cookie_file_name = os.tempnam('/tmp','dionysos')
        login_form_seq = [('userName', self.credentials['username']),('pwd', self.credentials['password']),('submit1', '%C5%DF%F3%EF%E4%EF%F2'),('loginTrue', 'login')]
        login_form_data = urllib.urlencode(login_form_seq)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.COOKIEFILE, cookie_file_name)
        curl.setopt(pycurl.COOKIEJAR, cookie_file_name)
        curl.setopt(pycurl.URL, 'http://dionysos.teilar.gr/unistudent/')
        curl.setopt(pycurl.POST, 0)
        curl.perform()
        curl.setopt(pycurl.URL, 'http://dionysos.teilar.gr/unistudent/login.asp')
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, login_form_data)
        curl.setopt(pycurl.WRITEFUNCTION, stringio.write)
        curl.perform()
        return (stringio.getvalue()).decode('windows-1253')
    
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


def get_student_credentials(username, password):
    '''
    Connects to dionysos.teilar.gr using pycurl, aggregates student's data.
    
    Returns credentials including:     username | password | last_name | first_name
                                    registration_number (A.M.) | semester | introduction_year
                                    labs (current registered labs) [DEPRECATED]
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

#        b1 = StringIO.StringIO()
#        conn.setopt(pycurl.URL, 'http://dionysos.teilar.gr/unistudent/stud_NewClass.asp?studPg=1&mnuid=diloseis;newDil&')
#        conn.setopt(pycurl.POST, 1)
#        conn.setopt(pycurl.POSTFIELDS, login_form_data)
#        conn.setopt(pycurl.WRITEFUNCTION, b1.write)
#        conn.perform()
#        soup_declaration = BeautifulSoup((b1.getvalue()).decode('windows-1253'))

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
#        soup2 = BeautifulSoup(str(soup1.findAll('tr')[8]))
#        credentials['school'] = str(soup2.findAll('td')[1].contents[0]).strip()
        soup2 = BeautifulSoup(str(soup.findAll('table')[15]))
        # introduction year is in type first_year - next_year season
        # if season is 'Εαρινό' we parse the second_year, else the first_year
        season = str(soup2.findAll('span','tablecell')[1].contents[0])[:2]
        if season == 'Ε':
            year = str(soup2.findAll('span','tablecell')[0].contents[0].split('-')[1])
        else:
            year = str(soup2.findAll('span','tablecell')[0].contents[0].split('-')[0])
        credentials['introduction_year'] = year + season
#        soup1 = BeautifulSoup(str(soup_declaration.findAll('table')[14]))
#        exam_msg = str(soup1.td.contents[0])
#        if exam_msg == 'ΝΑ ΜΗΝ ΞΕΧΑΣΩ ΝΑ ΚΑΝΩ ΑΠΟΣΤΟΛΗ ΤΗ ΔΗΛΩΣΗ ΣΤΗ ΓΡΑΜΜΑΤΕΙΑ ΚΑΙ ΝΑ ΕΠΙΒΕΒΑΙΩΣΩ ΤΗΝ ΕΠΙΤΥΧΗ ΑΠΟΣΤΟΛΗ ΤΗΣ !!!':
#            soup1 = BeautifulSoup(str(soup_declaration.findAll('table')[16]))
#        declaration = []
#        k = 8
#        tempspan = soup1.findAll('span', 'underline')
#        for i in xrange(len(tempspan)):
#            lab = str(tempspan[i].contents[0]).strip()
#            if lab.endswith('(Ε)'):#(u'\xce\x95')
#                declaration.append(lab)
#            k += 7
#        credentials['labs'] = declaration
        credentials['username'] = username
        credentials['password'] = password
        return credentials
    except:
        return {}


