# -*- coding: utf-8 -*-
'''
Created on Jan 11, 2016

@author: Oscar Hong
'''

import imaplib
import subprocess
from email import parser
from email import utils
import time
import re
import smtplib
import random
import config


class EmailGrade:
    '''
    classdocs
    '''

    def __init__(self, password: str):
        '''
        Constructor
        Starts a connection to gmail.
        Email address hardcoded, but password is taken as input.
        '''
        
        self.date_criterion = None
        self.email_addr = config.email_addr
        self.password = password
        
        self.conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.conn.login(self.email_addr, password)
        
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.email_addr ,password)
        
        
    
    def __del__(self):
        '''
        Destructor
        Closes the connection upton deletion of the class. 
        '''
        try:
            self.conn.close()
            self.conn.logout()
            self.server.quit()
        except:
            pass
    
    def _date_criterion(self):
        '''
        Returns a search criteria for the imap search method.
        The criteria grabs emails from the start date and onwards.
        '''
        return time.strftime('SINCE "%d-%B-%Y"')
    
    def get_start_time(self):
        '''
        Accessor method for the time where the class started to access the email.
        UTC Timestamp format.
        '''
        return self.start_time
    
    def set_start_time(self):
        '''
        Initializes the date searching criterion for emails and the start time in a UTC Timestamp format.
        '''
        self.start_time = int(time.time()) #Rounded down to the nearest second
        self.date_criterion = self._date_criterion()
    
    def email_list(self, prnt = True):
        '''
        Returns a list containing list representations of emails.
        The representations are comprised of the sender, the timestamp, the subject, and the body; in that order.
        '''
        list_of_email = []
        
        if self.date_criterion is None:
            self.set_start_time()
        self.conn.select()
        typ, data = self.conn.search(None, self.date_criterion, 'UNSEEN')#Filter for emails today that have not been seen
        #typ, data = self.conn.search(None, 'SINCE "12-Jan-2016"', 'SEEN')
        for num in data[0].split():
            typ, data = self.conn.fetch(num, '(RFC822)')
            e_list = []
            e_data = parser.BytesParser().parsebytes(data[0][1]) 
            e_sender = e_data['From']
            e_sender = utils.parseaddr(e_sender)[1]
            e_time = utils.mktime_tz(utils.parsedate_tz(e_data['Date'])) #utc timestamp
            e_subject = e_data['Subject'] #subject
            if e_data.is_multipart():
                body = ""
                for payload in e_data.get_payload():
                    if(payload.get_content_type() == "text/plain"):
                        body += payload.get_payload()   
                        
            else:
                body = e_data.get_payload()
            e_body = body
            #e_body = body.split("<html>")[0] #payload
            e_body = e_body.replace("=C2=A0", "")
            e_body = e_body.replace("=\r\n", "")
            e_body = e_body.replace("\r\n", "\n")
            #e_body = quopri.decodestring(e_body)
            #e_body = e_body.decode('utf-8')
            
            e_list.append(e_sender)
            e_list.append(e_time)
            e_list.append(e_subject)
            e_list.append(e_body)
                
            if prnt:
                print("Email Found:\nFrom: %s\nTime: %s\nSubject: %s\nBody:\n%s" % (e_list[0], e_list[1], e_list[2], e_list[3]))
                
            list_of_email.append(e_list)
        return list_of_email
    
    def compile_java(self, java_file: str):
        '''
        Compiles the java and returns the scores for that particular part. 
        Also prints out part of the results to a file.
        '''
        c_points = 0 #Compile points out of 2
        ct_points = 0 #Correct type points out of 1
        tc_points = 0 #Test case points out of 3
        score = [0, 0, 0]
         
        cmd = 'javac -d . ' + java_file + '.java'
        cmd1 = 'if exist test/' + java_file + '.class echo Compiled!'
        cmd2 = 'javac -d . ' + java_file + 'Test.java'
        cmd3 = 'if exist test/' + java_file + 'Test.class echo Compiled!'
        cmd4 = 'java test.' + java_file + 'Test ' + java_file
        cmd5 = 'del /Q test\*'
        
        initial_proc = subprocess.Popen(cmd5, shell = True)
        initial_proc.wait()
         
        proc = subprocess.Popen(cmd, shell=True, env = {'PATH': r'C:\Program Files\Java\jdk1.8.0_65\bin'})
        proc.wait()
        output = ""

        with open(java_file + '.java', 'r') as myfile:
            test_file = myfile.read()
         
        proc1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
        proc1.wait()
        output = proc1.stdout.read().decode('utf-8').strip()
        if output == "Compiled!":
            proc2 = subprocess.Popen(cmd2, shell=True, env = {'PATH': r'C:\Program Files\Java\jdk1.8.0_65\bin'})
            output = ""
            c_points += 2
             
            try:
                file = open((java_file + ".txt"), 'a')
                file.write('''Compiles ........................''' + str(c_points) + ''' out of 2
-Compiled Successfully (Standalone) 
 File Contents:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' + test_file + '''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''')
            except:
                print("Failed to open file")
            finally:
                if file is not None:
                    file.close()
             
            proc2.wait()
            proc3 = subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE)
            proc3.wait()
            output = proc3.stdout.read().decode('utf-8').strip()
             
            if output == "Compiled!":
                proc4 = subprocess.Popen(cmd4, shell=True, stdout=subprocess.PIPE, env = {'PATH': r'C:\Program Files\Java\jdk1.8.0_65\bin'})
                proc4.wait()
                result = proc4.stdout.read().decode('utf-8').strip()
                result = result.split("|")
                if len(result) == 2:
                    try: 
                        ct_points = int(result[0])
                        tc_points = int(result[1])
                    except:
                        pass
            else:
                try:
                    file3 = open((java_file + ".txt"), 'a')
                    file3.write('''Correct Return Type .............''' + str(ct_points) + ''' out of 1
-Could not run
Test Case .......................''' + str(tc_points) + ''' out of 3
-Could not run
''')
                except:
                    print("Failed to open file")
                finally:
                    if file3 is not None:
                        file3.close()
             
        else:
            try:
                file2 = open((java_file + ".txt"), 'a')
                file2.write('''Compiles ........................''' + str(c_points) + ''' out of 2
-Compilation failed
 File Contents:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' + test_file + '''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Correct Return Type .............''' + str(ct_points) + ''' out of 1
-Could not run
Test Case .......................''' + str(tc_points) + ''' out of 3
-Could not run
''')
            except:
                print("Failed to open file")
            finally:
                if file2 is not None:
                    file2.close()
        score[0] = c_points
        score[1] = ct_points
        score[2] = tc_points
        subprocess.Popen(cmd5, shell = True)
        return score
    
    def _grade_email(self, methodname: str, email_body: str):
        '''
        A method for grading the email itself.
        Simple check for Javadocs and method name.
        Rest of grading handled in the _grade method.
        '''
        jd_points = 0 #Javadoc points out of 2
        mn_points = 0 #Method name points out of 2
        
        javadocs = re.search('\/\*\*(.*?)\*\/', email_body, re.DOTALL)
        if javadocs is not None:
            javadocs = javadocs.group(0)
            jd_points += 1
            regex = re.compile('[^a-zA-Z]')
            javadocs = regex.sub('', javadocs)
            if (javadocs is not None) and (javadocs != ""):
                jd_points += 1
        
        method_declaration = re.search('.*?{', email_body, re.DOTALL)
        if method_declaration is not None:
            method_declaration = method_declaration.group(0)
            if methodname in method_declaration:
                mn_points += 2
        return (jd_points, mn_points)
            
    
    def _grade(self, assignmentname: str, methodname: str, email_body: str):
        '''
        Grades an email body.
        Email body placed into a class named after the variable assignmentname.
        Email is parsed by the _grade_email helper method.
        Java is compiled and evaluated by the compile_java method.
        Results are printed to a txt file named after the variable assignmentname.
        Returns the score.
        '''
        results1 = self._grade_email(methodname, email_body)
        jd_points = 0 #Javadoc points out of 2
        mn_points = 0 #Method name points out of 2
        c_points = 0 #Compile points out of 2
        ct_points = 0 #Correct type points out of 1
        tc_points = 0 #Test case points out of 3
        total_points = 0 #Out of 10
        
        jd_points = results1[0]
        mn_points = results1[1]
        
        if jd_points == 2:
            jd_found = 'found'
        else:
            jd_found = 'not found'
        if mn_points == 2:
            mn_found = 'found'
        else:
            mn_found = 'not found'
        try:
            file = open((assignmentname + ".txt"), 'w')
            file.write(assignmentname + '''
Auto-Graded....
Results (Tentative):
Javadoc .........................''' + str(results1[0]) + ''' out of 2
-Javadoc ''' + jd_found + '''
Method Name .....................''' + str(results1[1]) + ''' out of 2
-Method name (''' + methodname + ''')''' + mn_found + ''' 
''')
        except:
            print("Failed to open file")
        finally:
            if file is not None:
                file.close()
        
        try:      
            file2 = open((assignmentname + ".java"), 'w')
            file2.write('''package test;
    
public class ''' + assignmentname +''' {
''' + email_body + '''    
}''')
        except:
            print("Failed to write to test file")
        finally: 
            if file2 is not None:
                file2.close()
        
        results2 = self.compile_java(assignmentname)
        c_points = results2[0]
        ct_points = results2[1]
        tc_points = results2[2]
        
        total_points = jd_points + mn_points + c_points + ct_points + tc_points
        
        try:
            file3 = open((assignmentname + ".txt"), 'a')
            file3.write('''-------------------------------------------
Total ..........................''' + str(total_points) + ''' out of 10

Please send an email or talk to me if you believe there is a mistake. You can retry as many times as you like within the time limit.''')
        except:
            print("Failed to open file")
        finally:
            if file3 is not None:
                file3.close()
        
        return total_points
    
    def send_email(self, to_addrs: str, e_subject: str, e_body: str):
        '''
        Sends an email to the specified address with the specified subject and body.
        '''
        msg = 'Subject: %s\n\n%s' % (e_subject, e_body)
        self.server.sendmail(self.email_addr, to_addrs, msg)
    
    def keep_alive(self):
        try:
            status = self.server.noop()[0]
            if status != 250:
                self.server = smtplib.SMTP('smtp.gmail.com:587')
                self.server.ehlo()
                self.server.starttls()
                self.server.login(self.email_addr ,self.password)
        except:  # smtplib.SMTPServerDisconnected
            self.server = smtplib.SMTP('smtp.gmail.com:587')
            self.server.ehlo()
            self.server.starttls()
            self.server.login(self.email_addr ,self.password)
    
    def auto_grade(self, minutes: int, assignmentname: str, methodname: str, ta_address: str,prnt = True):
        if prnt:
            print("Starting....")
        self.email_list()
        self.set_start_time()
        seconds = minutes * 60
        current_time = time.time()
        print_counter = 0;
        grades = {}
        compilation = 'Grades for ' + assignmentname + '(Tentative)\r\n'
        
        if prnt:
            print("Started!!!")
        
        while (current_time - self.get_start_time()) < seconds:
            if (((current_time - self.get_start_time()) / 60) > print_counter):
                print_counter += .1
                if prnt:
                    print(str(minutes - ((current_time - self.get_start_time()) / 60)) + ' minutes left...')
            batch = []
            batch = self.email_list(prnt)
            for em in batch:
                e_sender = ''
                e_time = 0
                e_subject = ''
                e_body = ''
                name = ''
                grade = 0
                response = 'An Error Has Occured'
                
                e_sender, e_time, e_subject, e_body = em
                
                regex = re.compile('[^a-zA-Z0-9]')
                filtered = regex.sub('', e_subject).lower().strip()
                if 'ics211' in filtered and not filtered.startswith('re'):
                    if prnt:
                        print("Email Valid: ")
                    name = e_subject.split(":")
                    if len(name) > 1:
                        name = name[1]
                    else:
                        name = name[0]
                    name = name.strip()
                    grade = self._grade(assignmentname, methodname, e_body)
                    with open(assignmentname + '.txt', 'r') as myfile:
                        response = myfile.read()
                    self.keep_alive()
                    self.send_email(e_sender, ('RE: ' + e_subject), response)
                    if prnt:
                        print("Grade: " + str(grade))
                    grades[name] = grade
            current_time = time.time()
                    
        for name in grades:
            compilation += name + ':' + str(grades[name]) + '\r\n'
        self.keep_alive()
        self.send_email(ta_address, ("ICS 211: " + assignmentname + " Grades"), compilation)
        if prnt:
            print("Time up")
        

    