#!/usr/bin/python

from subprocess import *
import subprocess
cmd = "ls"
#files = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
files = subprocess.call(cmd, shell=True)#stdout=subprocess.PIPE)
#(output, err) = files.communicate()
#(output, err) = newf.communicate()
#val  = list(output)
#print files
#for i in tuple(output):
    #print "The value of file", i
#output = list(files)
#print output


proc = subprocess.Popen('ls', stdout=subprocess.PIPE)
output = proc.stdout.read()
print output


newval = subprocess.check_output('ls')
#newval
