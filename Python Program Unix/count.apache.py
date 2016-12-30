#!/usr/bin/python

import os
import re
reading = open("access_log-20161204")
chek = reading.readlines()
reading.close()
########## TO EMPTY THE FILE ######
with open("data", 'w'): pass
for i in chek:
    #out = re.search(r'([0-9]{2})', i) OORR Below one also correct
    #print i
    out = re.search(r'(([2])(\d)([0]))', i)
    #out = re.search(r'((^[2])(\d)([0]))', i)
    print out.group(1)
    wr = out.group(0)
    if out:
        #for inp in out:
        newf = open("data", "a+")
        newf.write("Repeasted\n")
        newf.close()

count = len(open("data").readlines(  ))

print "Total count", count
#http://www.guru99.com/functions-in-python.html




#print total
        #val = count(out)
        #print "Pass"
        #print "Total times access is " val
        #print "The Anumber of times website access", i
