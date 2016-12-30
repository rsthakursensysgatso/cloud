import re
lst = ["Ravin", "Devops", "Devops","Test","india","Ravin","Ravin","Ravin","Ravin","Ravin","Ravin"]

#dup = []
tl = []
for i in lst:
    val = re.search(r'R([a-z]+)', i)
    if val:
        res = val.group(0)
        tl.append(res)
print tl
print len(tl)  ##### GREATTTTT  ORR BELOW ONE
print tl.count(res) ##### GREATTTTT
