#!/usr/bin/python

from subprocess import *
import subprocess
cmd = "ls"
result = "/mnt/cifs/result"
p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE)
#files = subprocess.call(cmd, shell=True)
output = p.stdout.read()

ipconfig = subprocess.check_output("ifconfig")
#print(ipconfig)
print ipconfig


####### REDIRECT THE OUTPUT OF THE COMMAND
import os
f = os.popen('date')
now = f.read()
print "Today is ", now
f.read() > result
#subprocess.call("date") > result


p = subprocess.Popen('echo `date` > /mnt/cifs/result', stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print "Today is", output
#output > "/mnt/cifs/result"


p = subprocess.Popen('date', stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print "Today date  is ", output
