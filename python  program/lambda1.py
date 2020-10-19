def newf(var):
    out=[]
    for i in var:
        out.append(i)
    return out
    #print newf(["Ravi","Devops","Cloud"])
print newf(range(10))
#var = lambda x,y: x if y == 2 else print "Thakur"
#print var(2,3)


def myt(put):
    linux=[]
    for i in put:
        if i > 5:
            linux.append(i)
    return linux
    #return myt
print myt(range(20))

filt = lambda value: value % 2 ==0 ## statemet true value will go like 2 , 4 ,6
even = lambda out: filter(filt, out)## filter only even out from range 20
print even(range(20))


odd = lambda value: value % 2 ==1 ## statemet true value will go like 2 , 4 ,6
even = lambda out: filter(odd, out) ## filter only odd out from range 20
print even(range(20))
