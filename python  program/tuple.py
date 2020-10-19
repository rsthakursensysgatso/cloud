#!/usr/bin/python

var = ("Devops", "cloud", "rising")     + ("Noew", "Addition")
tup = ("Devops", "cloud", "rising")
tup1 = ("Devops", "cloud", "rising")

print (var)
print (var[0:2])

print "Addition result =>", (var)

### Looping of the tuple

for i in var:
    print "The value of tupple is as =>", i
## Member ship in tuple

    print ("Devops" in var)

    print ("thakur" in var)
else:
    print ("All done")

## check the length of tuple

#    print "The length of var tupple is ==>", (len(var()) ## to check full lenght of tup;e
    print "The length of the variable is ==>",(len(var[0:2])) ## to chech number of element between some range

    print "The value of the two tuple is same so return 0 ===> ", (cmp(tup,tup1)) ## Compare two tuple and will return 0 if mataches else retur 1 or some other number

    print "The value of the two tuple is same so return 1 ===>", (cmp(tup,tup1)) ## Compare two tuple and will return 0 if mataches else retur 1 or some other number


## change in the tuple is not possible see below example ==> 'tuple' object does not support item assignment

var[2] = ("Change it")

## Try to delete the element/object of tuple => Error we will is  tuple' object doesn't support item deletion

del var[0]
