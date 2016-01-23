'''
Created on Jan 17, 2016

@author: Standard
'''

import email_grade
from getpass import getpass
import sys
import time
import config
import subprocess
import quopri
import base64

if __name__ == '__main__':
    
    #eg = email_grade.EmailGrade('twentyoneguns')
    #print(str(eg.email_list()))
    
#     sample = '''/**\r\n     * A simple method that returns a string with a hello world message.\r\n     * @return The string "Hello World!!!".\r\n     */\r\n    public static String helloWorld(){\r\n        return "Hello World!!!";\r\n    }\r\n'''
#     print(eg._grade(assignmentname = config.assignmentname, email_body = sample, methodname = config.method))
    
     sample = '''/*** Something
*/
public static String helloWorld(){ return "Correct String=
!";
}'''
     decoded = quopri.decodestring(sample)
     print("quopri decoded: " + str(decoded))
     decodedx2 = decoded.decode("utf-8") 
     print("decoded quopri: " + decodedx2)
     
     b64decode = base64.standard_b64decode(sample)
     print("decoded b64: " + b64decode)
     
