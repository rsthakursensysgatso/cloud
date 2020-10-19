try:
## WRITE operation
    fileop = open("ravi.txt", "w")
    for i in xrange(100):
        fileop.write("Ravinder Devops Engineer\n")
    fileop.close()
except IOError as Devops:
    print "Ravinder"
## READ operation the first 16 character from file
reading = open("ravi.txt")
out=reading.read(164)
print out ##  print (out)
reading.close()

## Read full file rather than first few charactoer if we dont specify the number ()

reading = open("ravi.txt")
chek = reading.readline()
print chek

## read full lines

newread = open("ravi.txt")
lout = newread.readline()
print lout
newread.close()

## but readlines will return the output in string line format

chkrlines = open("ravi.txt")
#while  pread != "":
pread = chkrlines.readline()
print pread
chkrlines.close()
