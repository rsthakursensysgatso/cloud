import re

dig = '24.23.45.24.45'
#print dig
out =re.search(r'(\d{1,2}\.)+', dig)
print out.group(0)

var = 'John Rocker'
var1 = 'John   T Rcoker'

val = re.search(r'John(\s+)(\w+)?(\s+)(\w+)', var1)
print val.group(0)


###### Quatifying a group
vak = re.search(r'John(\s+)(\w+)', var)
print vak.group(0)

##### Choice to find the value of variables using and |
newval = 'Devops 234work For '

chk = re.search(r'^Dev(\w+)', newval)
print chk.group(0)

#chk = re.search(r'^Dev(\w+)(\s+)((\d+)|(\w+))(\s+)(\w+)(\s+)', newval)
chk = re.search(r'^Dev(\w+)(\s+)((\d+)|(\w+))', newval)
print chk.group(0)

#pattern = r'(\d+)'
test_str = [
          'Ravinder'
          '1983'
          'House'
          'Number'
          'Sector'
          '51D'
          'Chandigarh'
          'Jakarta'
          'Devops $#@#%'
]
#print pattern
for i in test_str:
    #if re.search(r'(\d+)', i):
    if  re.search(r'(\d+)', i):
        out = re.search(r'(\d+)', i)
        print "Get the desired pattern", out.group(0)
    else:
        print "Not Get the value"

for i in test_str:
    #if re.search(r'(\d+)', i):
    if  re.search(r'(\d+)(\s)', i):
        out = re.search(r'\d\d\s', i)
        print "Get the desired pattern", out.group()
    else:
        print "Not Get the value"

for i in test_str:
    matchobj = re.search(r'(\d+)(\w+)', i)
    if  matchobj:
        print "Get the desired pattern", matchobj.group(0)
    else:
        print "Not Get the value"

pt = r'(\w+)'
for i in test_str:
    matchobj = re.search(pt, i)
    print matchobj.group(1)
    print "string, %s;"
