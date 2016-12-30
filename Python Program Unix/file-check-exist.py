#!/usr/bin/python

import subprocess
import sys
#from os import *
import time
import re
import shutil
import os, sys

loc = os.getcwd()
print "Working directory", loc
if os.path.isfile("yahoo"):
    print "file exist and its location is ", loc
else:
    print "Not exist and creating & writing the files"
    var = open("yahoo", "w")
    data = var.write("CLUD COMPUTING\n")
    var.close()
#### for directory check &list all file in the directory
lis = os.listdir(loc)
print "list of directory", lis

for i in lis:
    if os.path.isdir(i):
        print "The directory", i
    else:
        print "it is file", i


####### for file check

for i in lis:
    if os.path.isfile(i):
        print "It is file", i
    else:
        print "Rest of them are directories", i
