#!/usr/bin/python

import sys
import os
import time
import re
port="/root/python/port"
a=os.popen('netstat -ntpl |grep  8080').read()
#print "http connections ",a > open( 'logfile.log', 'w')
fileop = open("ravi.txt", "w")
fileop.write(a)
fileop.close()

fileops = open("ravi.txt", "r")
red = fileops.read()
val = red.split()
print "Each value of split element is ", val
for i in val:
    #pat = re.search(r'(\w{2})(\d?)', i)
    pat = re.search(r'([a-zA-Z][a-zA-Z][a-zA-Z]\d)', i) ## to match the alphabet and digit
    pat2 = re.search(r'([a-zA-Z][a-zA-Z][a-zA-Z]\d?)', i) ## to match the alphabet and digit optional using ?
    #print pat.group(0)
    if pat:
        print pat.group(0)
    if pat2:
        print pat2.group(0)
    #chk = pat.group()
    #print chk
#    com = "tcp6"
    #if pat == com:
#        print "The value of ", pat


#out = re.search(r'Rav.*', red) #


    #out = re.search(r'(\w+?\d+?)(\s)', i)
    #if out:
#        print out.group(0)


#for i in test_str:
    #matchobj = re.search(r'(\d+)(\w+)', i)
    #if  matchobj:
#        print "Get the desired pattern", matchobj.group(0)#
    #else:
        #print "Not Get the value"

#pt = r'(\w+)'
#for i in test_str:
#    matchobj = re.search(pt, i)#
    #print matchobj.group(1)
    #print "string, %s;"


#sobprocess.call( ['ls'] stdout = open( 'logfile.log', 'w') )
#input('Press ENTER to exit')

