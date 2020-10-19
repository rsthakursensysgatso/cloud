#!/usr/bin/python
import subprocess

cmd = "cat /etc/passwd"
p = subprocess.Popen(cmd, shell=True)
output = p.stdout.readlines()
#print output
