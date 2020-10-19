#!/usr/bin/python

from os import *
import time
import re
import shutil
import os, sys

input_filename = raw_input("Enterfile ")
#base_name, extension = os.path.splitext(input_filename)
terr="newfile"
output_filename = terr + '.asd'
shutil.copy(input_filename, output_filename)
