import re

arry = ["12","Devops","98"]
comp = [n for n in arry]  ## list comprehenstion return the list in the same form
print comp


useo = [12,4,5]
out= map(lambda x: x*x, useo)
print out

## OR IN ONE LINE LAMBDA fucntion

print map(lambda x: x**x, useo)

oth = ["Devop","Germay","Cloud"]
print map(lambda x =[]: x, (oth))

nums = [34,34,54,67,7]
out = []
for val in nums:
    if val%2 == 0:
        out.append(val)
print out

### ONE LINE ABOVE FUNCTION
print filter(lambda x: x%2 == 0 , nums)







##### MORE MAP & FILTER EXAMPLES
#import re

#text = 'This is a black ant'
#pattern = re.search(r'a[nr]t', text)
#tp = ["PROD", "TEST", "DEV", "Ravi"]
####### http://www.thegeekstuff.com/2014/07/python-regex-examples/  #####3
tp = ["DEV CLouder"] ## OR tp = ('DEV CLouder')
#tp = 'DEV CLouder'
#print "Each value of tp", i
for i in tp:
    print "The value of tp variable", i
    out = re.search(r'DEV', i) ######## TO search the value of DEV in the tupple
    var1 = out.group(0)
    #print var1
#print out.group()
    #var = ('DEV')
    val = "DEV"
if val == var1:
    print "Find the value of i", val
    #print  i.group()
else:
    print out.group()
    print "Not working laaa"

tp = ["DEV CLouder"]
print map(lambda val:  tp[0:14] == 'DEV CLouder', tp)
