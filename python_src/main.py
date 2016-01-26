# -*- coding: utf-8 -*-
'''
Created on Jan 11, 2016

@author: Oscar Hong
'''

from getpass import getpass
import email_grade
import sys
import config

if __name__ == '__main__':
    '''
    Documentation goes here
    '''
    
    timelimit = 0
    '''
    if len(sys.argv) < 2: #use timestamp as name of file for storing grades if name not specified in command line
        filename = str(time.time()) + '.txt'
    else: #get name of file from command prompt for storing grades
        filename = sys.argv[1] + '.txt'
    '''
    while True: #get password
        password = getpass('Enter Email Password (enter "quit" to end program): ')
        if password == 'quit':
            print("Terminated.")
            sys.exit()
        try:
            eg = email_grade.EmailGrade(password)
            break
        except: 
            print("Unable to connect. Try Again.\n")
    
    while True: #get time limit
        try:
            timelimit = int(input('Specify Length of Time in Minutes: '))
            print('Input: ' + str(timelimit))
            print('Type: ' + str(type(timelimit)))
            break
        except:
            print("A problem has occured. Try Again.\n")
    
    eg.auto_grade(timelimit, config.assignmentname, config.method, config.TA, True)
    
    