#!/usr/bin/python

import os
import re
import fileinput
#for chek in fileinput.input(["access_log-20161204"]):

val1 = r'([2])(\d)([0])'

reading = open("access_log-20161204")
chek = reading.readlines()
reading.close()
########## TO EMPTY THE FILE ######

def countk(varr):

    for i in chek:

        out = re.search(varr, i)
        print out.group(1)
        wr = out.group(0)
        if out:
            newf = open("data", "a+")
            newf.write("Repeasted\n")
            newf.close()

countk(val1)
count = len(open("data").readlines(  ))
print "Total count", count

with open("data", 'w'): pass


#http://www.guru99.com/functions-in-python.html




#print total
        #val = count(out)
        #print "Pass"
        #print "Total times access is " val
        #print "The Anumber of times website access", i
