import re

li = ["Ravin", "Devops", "Devops","Test","india"]
with open("data", 'w'): pass
for x in set(li):
    li.remove(x)
    out = list(set(li))
    print "Total count", out
    if out:
        newf = open("data", "a+")
        newf.write("Repeasted\n")
        newf.close()

count = len(open("data").readlines(  ))
print "Total count", count


li = ["Ravin", "Devops", "Devops","Test","india"]
y=list(li)

#print y



lst = ["Ravin", "Devops", "Devops","Test","india","Ravin","Ravin","Ravin","Ravin","Ravin","Ravin"]

#dup = []
tl = []
for i in lst:
    val = re.search(r'R([a-z]+)', i)
    if val:
        res = val.group(0)
        tl.append(res)
print tl
print len(tl)  ##### GREATTTTT
print tl.count(res) ##### GREATTTTT


### COUNT EACH ELEMENT number of times in the list ######
my_dict = {i:lst.count(i) for i in lst}
print my_dict


MyList = ["a", "b", "a", "c", "c", "a", "c"]
my_dict = {i:MyList.count(i) for i in MyList}
print my_dict     #or print(my_dict) in python-3.x
