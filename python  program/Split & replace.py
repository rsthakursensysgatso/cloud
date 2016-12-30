myvar = ["Devops", "Linux", "Cloud"]

for i in myvar:
    print "Each element of List is ", i
    if i == "Devops":
        out = i.split('o')
        for res in out:
            print "each split element is ", res
            if res == "Dev":
                val = i.replace('Dev','Hello')
                print val
            elif res == "ps":
                val1 = i.replace('ps','World')
                print val1

        #print out

x = range(2,20)
newv = []
for i in x:
    if i % 2 == 0:
        print "the value of x", i
        newv.append(i)
        print newv  ### IT will generated the list each time element is even

val = newv.count(2)
print val+12
#for i in newv:
    #print i

    #else:
        #print "\n"


#res = newv.count('2')
#print newv
#print res
