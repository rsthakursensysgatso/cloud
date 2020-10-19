import re
class store:
    incremt = 22
    items = 0
    def __init__ (self, item1,item2,place,costt):
        self.item1 = item1
        self.item2 = item2
        self.item3 = item1+ " "+item2+ " "+place
        self.costt = costt
        store.items += 1

    def latest(self):
        if (self.item1 == 'apple'):
            print "Fist item is ", self.item1
        elif(self.item1 != 'apple'):
            print "Fist item is not", self.item2
        return self.item1
    def cst(self):
        #incremt = 55
        print self.costt
        #self.costt = int(self.costt * self.incremt)
        self.costt = int(self.costt * store.incremt)
        #return self.costt

print (store.items) ## it will be zero because the
rate = store('apple','code','jkt','45')
rate1 = store('app','code','jkt','56')
rate.cst()
rate.incremt = 4
#rate1.incremt = 6
print (rate.incremt)
print (store.incremt)
print (rate1.incremt)

#print rate.cst()
#print rate1.cst()
print (rate.__dict__)
print (store.items)

print rate.cst()
print rate.latest()
print rate1.latest()
