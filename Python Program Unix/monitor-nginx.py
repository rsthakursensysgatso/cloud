#!/usr/bin/python

import sys
import os
import time
import re

a=os.popen('netstat -ntpl |grep nginx| grep 80|tail -1').read()
print a
if a:
    print "Nginx is running"
else:
    x = 0
    while x < 3:
        time.sleep(4)
        print "Nginx not running starting"
        b=os.popen('service nginx restart').read()
        print b
        x +=1
