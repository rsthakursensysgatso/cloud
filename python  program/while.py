i=2
while (i < 10 ):
    print i;
    i +=1 # counter increment
else:
    print "Counter value has reached ", i


while False:
    print i
    i +=1
else:
    print "The value has reached"
out = re.search(r'(\w+?\d+?)(\s)', i)
