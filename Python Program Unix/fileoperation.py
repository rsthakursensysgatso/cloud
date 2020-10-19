#!/usr/bin/python
import os
from subprocess import *
##########3https://jimmyg.org/blog/2009/working-with-python-subprocess.html

result = "/mnt/cifs/result"
f = os.popen('cat /etc/resolv.conf')
now = f.read()
print "Today is ", now
#f.read() > result
now > result
#subprocess.call("date")

#for i in  result:
    #ip = "202.73.99.4"
    #if i == "202.73.99.4":
    #    print "Got the dns name"
    #else:
    #    print "Not got it"
