#!/usr/bin/python
from subprocess import *
import subprocess
import sys
import os
import time
import re
import shutil


port="/root/python/port"
a=os.popen('ls /tmp/files').read()
#print "http connections ",a > open( 'logfile.log', 'w')
fileop = open("ravi.txt", "w")
fileop.write(a)
fileop.close()

ser = r'^[a-z]{3,9}c$'
pattern = r'^\d+\.\d\d'
val = r'a+x?b*x?c{1,3}x?'

fileops = open("ravi.txt", "r")
red = fileops.read()
val = red.split()
print "Each value of split element is ", val
for i in val:
    pat = re.search(r'^(\d+)([a-zA-Z]+$)', i)
    if pat:
        print "Pat value", pat.group(0)
        file1=pat.group(0)
        cmd ="mv"
        cre= "mkdir"
        dire="test1"
        cr=os.popen('mkdir dire')
        #ORRRR
        #shutil.remove(dire)
        shutil.copy(file1, 'dire')
        ### OORRR
        ##shutil.copy(file1, 'test1')
    pat1 = re.search(r'([a-zA-Z]+)(-)\d(-)\w', i)
    #print "pat 1", pat1.group(0)
    if pat1:
        #pat1 = re.search(r'[a-zA-Z]+\-\-\w')
        print "Pat1 is ", pat1.group(0)
        var=pat1.group(0)
        test2='clddiar'
        #paht= "/tmp/test/"
        cr=os.popen('mkdir test2')
        #shutil.copy(var, 'test2') ORRRRRR BELOW
        shutil.copy(var, "/tmp/test/")
        #shutil.copy(var, 'paht')

 #print "MYPATH:", os.path.join('', 'etc', 'init.d')
cwdir = os.getcwd()
dirr = "/mnt/mob/app"
myfolder = os.path.join (cwdir, "mob","app")
print "value of ", myfolder
os.makedirs(myfolder)
