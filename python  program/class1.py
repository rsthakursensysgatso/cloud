
strp = "Devops aws rockes"

out = strp.upper()
tl = len(strp)
print tl
print "THe value of strp is", out

stp = range(5,10)
leng = len(stp)
print leng

class name:
    def ravi(self, nm,sec):
        self.nm = nm
        self.tm = 5
    def test(self):
        #print(self.nm, self.tm)
        print(self.nm)
        if ( self.nm == 'Dev'):
            print "Got the value Dev"
        #elif ( self.nm == "OPS"):
        elif (self.nm == 'OPS'):
             print "Got the value OPS"

nme=name()
nme.ravi("OPS","Thakur")
nme.test()
#nme.test()
