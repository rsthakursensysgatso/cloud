#!/usr/bin/python
from subprocess import *
import subprocess
#call("ls")
cmd = "ls -l"
res = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#res_status = res.wait()
out = res.call.stdout
print "The output of the commnad", out
#print "The exit status of the ls -l command is", res_status
#print "The exit status of the ls -l command is", res.call.stderr
