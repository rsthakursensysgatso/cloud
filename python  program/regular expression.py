import re
text = 'This is a black ant'
pattern = re.search(r'a[nr]t', text)
print pattern.group(0)

fileop = open("ravi.txt", "w")
for i in xrange(5):
    fileop.write("Ravinder Devops Engineer\n")
fileop.close()
#files = open.files
files = open("ravi.txt", "r")
val=files.readline()
print val
out = re.search(r'Ravi', val)
print out.group(0)


var = ["Devop", "Cloud" , "Ting"]
print str(var)

pat = 'see the value of world top IT companies'
###### match only find fist value while search find all string
#ot = re.match(r'companies', pat)
#ot = re.match(r'the', pat)
ot = re.match(r'(\w+)', pat)### for the integet \s+

print ot.group(0)
print ot.start()

pat = 'see the value of world top IT companies'
ot = re.search(r'of', pat)
print ot.group(0) ### to check the first value of string ONLY
print ot.start() ## start location of find pattern
print ot.end() ### end  location of find pattern
#


#####
