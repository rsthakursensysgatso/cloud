#!/usr/bin/python
import subprocess
cmd = "/usr/bin/netstat -ntpl|grep  tcp"

## run it ##
p = subprocess.Popen(cmd, shell=True, stdin=oup stderr=subprocess.PIPE)
print oup
## But do not wait till netstat finish, start displaying output immediately ##
while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()

####### TEST
