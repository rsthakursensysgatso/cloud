#!/usr/bin/python


var1 = "Ravinder"
var2 = "Devops"

#out = var1/var2

try:
    out = var1/var2
    print out
except TypeError:
    print "Not the write code change the value to integer"

print "Change it please"


var3 = "ra"
var4 = 6

#res = var3/var4
#print res
try:
    res = var3/var4
except TypeError:
    print "Name Error Correct It Please"
