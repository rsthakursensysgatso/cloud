#!/usr/bin/python
from subprocess import *
import subprocess
#p1 = Popen(["dmesg"], stdout=PIPE)
#p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
#p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
#output = p2.communicate()[0]
#print p1
#print output
#print output

output=check_output("dmesg | grep sda", shell=True)

print output

#To also capture standard error in the result, use stderr=subprocess.STDOUT:

subprocess.check_output("ls non_existent_fileddf; exit 0",stderr=subprocess.STDOUT,shell=True)

try:
    #out_bytes = subprocess.check_output(['cmd','arg1','arg2'])
    out_bytes = subprocess.check_output("ls non_existent_fileddf;exit 0")py#; exit 1",stderr=subprocess.STDOUT,shell=True)

except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    code      = e.returncode   # Return code
