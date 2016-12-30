test = lambda a,b: a+b
print (test(3,6))


#ravi = lambda x,y: x if y > 0
#print ravi(2,3)

ravi = lambda x,y,z: x + y +z
print ravi(4,56,34)

square = lambda x:  x*x
print square(4)

removetest = lambda inp: set(inp)
print removetest("CHECCCCCCCCCCD")

# convert the string into the integer
convert  = lambda result: map(int, result)
print convert(["12","34","45","54"])

def newf(var):
    #out=[]
    for i in var:
        print i
        out.append(i)
        #return out
    #print newf(["Ravi","Devops","Cloud"])
        print newf(range(10))
#var = lambda x,y: x if y == 2 else print "Thakur"
#print var(2,3)
