import re
lt = ["Make It Dev"]
    #out = i.partition('M')
for i in lt:
    val = re.search(r'M', i)
    f1 = val.group(0)
    val1 = re.search(r'a',i)
    f2  =  val1.group(0)
    val3 = re.search(r'k', i )
    f3  = val3.group(0)
    val4 = re.search(r'e', i )
    f4 = val4.group(0)
    a = f3.upper()
    b = f4.upper()
    s = ''
    #fv = (f1,f2,a,b)
    fv = (a,f2,b,f1)
    print s.join(fv)
    ######## ORRRRRRRRR
    print ''.join(fv)

############formating

print " %s and second value of formating is %s" %(a,b)
print "{} and second value of formating is {}".format(f4,b)
