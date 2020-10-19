import re

#ser = r'[a-z]{2,3}\d+?'
#ser = r'[a-z]+\d+'
ser = r'^[a-z]{3,9}c$'
pattr = [ 'devops',
          'thakur',
          'linux',
          'aacbsdc',
          'werd23',
          'sdferc'

]

for i in pattr:
    if re.search(ser, i):
        print '"%s"The value of match is "%s"' % (ser, i)
