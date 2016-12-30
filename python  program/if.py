
a = 2
b = 6/2

if b % 2 <= 2:
    print "Number is less than", b

else:
    print "Now fine"

if b == 0:
    result = b % 3 ## %  gives the remainder
    print "The value of result is ", result

else:
    print "Calculation done"

now = ["Test", "Value", "List", "Check"]

print "Each value of list", now[0]
for i in now:
    #print i
    j = 'List'
    if i == j:
        print "Found the required value", i
        break   ######## BREAK THE LOOP WHEN FOUND
    else:
        print "not found yet and found", i
