#!/usr/bin/python

import subprocess
import sys
from os import *
import time
import re
import shutil
import os, sys

cwdir = os.getcwd()
myfolder = os.path.join (cwdir, "mob","app")
#print "value of ", myfolder
#os.makedirs(myfolder)

newdir = "/mnt/app/test"
#path=os.path.exists('newdir')
#print path
#if not os.path.exists('newdir'):
if os.path.exists(newdir):
    print "Directory not already exist  create it", newdir

#os.makedirs(newdir)
else:
    print "Not Exist Creating now", newdir
    os.makedirs(newdir, 0777)


### EXCEPTION ERROR HANDLING
try:
    print "not error"
except Exception:
    pass
    #os.makedirs(newdir)
path = "/mnt/thakur"
dirr = os.getcwd()
print dirr
if not  os.path.exists(path):
    print "Not  exist & Creating", path
    os.makedirs(path)
else:
    print "Directory structure exist", path


###### ORRRRRRRRR


newval = "/mnt/cloudd"
dirr = os.getcwd()
print dirr
if   os.path.exists(newval):
    print "Directory Exist", newval

else:
    print "Directory structure creating", newval
    os.makedirs(newval)



#newp = "/ravi/thakur"
#print newp
#if  os.path.exists(newp):
#    print "Path not exist create", newp
    #os.makedirs(newp, 0777)
#else:
    #print "Path exist"
    #os.makedirs(newp, 0777)
