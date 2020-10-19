import re

fil = open("ravi.txt")
red = fil.read()
#print red
print red
#out = re.search(r'\w[A-Z]*[a-z].*Rav.*', red) #'Ravinder SIngh')
out = re.search(r'Rav.*', red) #'Ravinder SIngh')
print out.group(0)

#res  = re.search(r'(\w+)(\s+)(Ravinder )$', red) #'Ravinder SIngh')

fil = open("ravi.txt")
red = fil.read()
#print red
for i in red:
    #res  = re.search(r'(\w+)(\s+)(Ravinder )$', red)
    #print red
    #res  = re.search(r'(\w+)(\s+)(world)', red)
    res  = re.search(r'world', red)
    par = 'world'
    if res.group(0) == par:
        print "The value  res & red", res.group(0)
    else:
        print "NOT FOUND", res.group(0)

#fil = open("ravi.txt")
#red = fil.readlines()
##match = re.search(r'This.*', ravi.txt, re.DOTALL)
#print match.group(0)
