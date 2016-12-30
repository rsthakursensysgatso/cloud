#http://www.thegeekstuff.com/2013/06/python-list/?utm_source=feedly
a = [0, 2, 2,4,5,6,7, 3]

a.remove(2)
print a

out = a.index(3)  ## search the index value of element 3
print "search the index value of element 3 ===> ", out


a.insert(8,"400") ### insert element on 8th posistion

print "insert element on 8th posistion ==>", a


a.remove(5) ## Remove 5th element
print "Remove 5  element that is ", a
