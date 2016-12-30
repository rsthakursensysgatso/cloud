#!/usr/bin/python

## here we will see how we can extract only key from dictionary

var = {56:90,56:67,78:23}
result = {}
for ex in var:
    print "The value of all key", ex
else:
    print "All done"


for i in var:
    result[var[i]] = i
    print (result)

## GREAT question if we have two values are same in the dictornay then only last one will be changes to values to key & vice versa

test = {34:56,5:67,99:45,12:45}
newres = {}

for i in test:
    newres[test[i]] = i
    print (newres)




newvar = {"sample":[1,2,4,5], 'a':'tar'}
dict = {"sample":[1,2,4,5], 'a':'tar'}

print (newvar)

newvar.clear()
print (newvar)


print newvar.has_key('a')
print newvar.has_key('sample')


print (newvar.items()) ## key value out in form of tuple form
print (dict.items()) ## output of tuple value form
print (dict.keys()) ## output of keys
print (dict.values()) ## output of values


dic  = {"Ravinder":"Thakur", "Next": "Steps"}

for i in dic:
    print "The key value of dic", dic[i]
    out = dic[i]
    print out

    print dic.has_key('Ravinder')
    print dic.has_key('Next')

    print dic.keys()
    print dic.values()
