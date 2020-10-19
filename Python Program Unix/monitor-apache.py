#!/usr/bin/python

import sys
import os
import time
import re

print "This script will Work perfect only when nginx running and need modification"
port="/root/mnt/port"
a=os.popen('netstat -ntpl |grep nginx| grep 80|tail -1').read()
#print "http connections ",a > open( 'logfile.log', 'w')



fileop = open("process", "w")
fileop.write(a)
fileop.close()

content = open("process", "r")
newvar = content.read()
content.close()
print newvar

#for i in newvar:
    #print "Each value of content is ",
#portt1 = re.search(r'(:)(:)(:)(\d+)', newvar)
#print portt1.group(0)
portt = re.search(r'(\d)(\d)', newvar)
print portt.group(0)
varr = portt.group(0)
if portt:
    print "Service running ", varr
else:
    print "Service not running start it", varr
    b=os.popen('service nginx start').read()
    print b
