#!/usr/bin/python

import fileinput
import re

url1 = r'(button)'
url2 = r'(home)'
url3 = r'(bground1)'
url4 = r'(search)'

var1 = r'(david)'
var2 = r'(alex)'
var3 = r'(robert)'
eror = r'(Error)'

listt = []
resl = []

def repp(newv):
    for line in fileinput.input('access.log'):
            out = re.search(newv, line)
            if out:
                listt.append(out.group(0))
                final = listt.count(out.group(0))
    return final

tpurl = repp(url1)
tpurl2 = repp(url2)
tpurl3 = repp(url3)
tpurl4 = repp(url4)

mydict = {'button':tpurl,
          'home':tpurl2,
          'bground1':tpurl3,
          'search':tpurl4}

for key, value in sorted(mydict.iteritems(), key=lambda (k,v): (v,k)):
    website = sorted(mydict.keys())
    totalcount = sorted(mydict.values())

print "The most Visited url name is %s.html, and its count is ---> %s" %(website[-1], totalcount[-1])

uniqu1 = repp(var1)
uniqu2 = repp(var2)
uniqu3 = repp(var3)

mylist = [uniqu1, uniqu2, uniqu3]
mylist.sort()
print "David Visited ->", mylist[0]
print "Alex  Visited ->", mylist[1]
print "Robert  Visited ->", mylist[2]


reserr = repp(eror)
print "Total number of times Error occured -->", reserr
