class store:

    def __init__ (self, item1,item2,place):
        self.item1 = item1
        self.item2 = item2
        self.item3 = item1+ " "+item2+ " "+place
    def latest(self):
        if (self.item1 == 'apple'):
            print "Fist item is ", self.item1
        elif(self.item1 != 'apple'):
            print "Fist item is not", self.item1


stritm = store('appl','mango','shelf')
stritm2 = store('Bread','Bananda','Fllor')
print(stritm.item3)
stritm.latest()
stritm2.latest()
print(stritm.item1)### access the variable defined in the instance for class
print stritm.item1  ### access the variable defined in the instance for class
