#!/usr/bin/python

from subprocess import *
import subprocess
cmd = "ls -l"
files = subprocess.call(cmd, shell=True)
#print files

newf = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
#print newf.stdout
(output, err) = newf.communicate()
#print output

for i in output:
    print "THese are the files", i

#print newf.stdout ## by default it will return none
#print newf.stderr
#print newf.poll() ### for the exist status it will poll the process and return exit status
### if exit status of poll show nothing that it means process running
newf.wait() ## wait for the process to get kill
#newf.terminate() ## to terminate the runnign process
#newf.pid() ## to check the process of running process under command

#print newf.stdout
