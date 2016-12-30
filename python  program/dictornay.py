
var = dict()

print (var)


var = dict()

print (var)  ## it will show that it is dictory because it is preseneted {}

val = {"Ravinder" : "Thakur", "Devops" : "Cloud"}

print (val)
print (val["Ravinder"])  ## The value of key "Ravinder " is "Thakur"
print (val["Devops"])  ## The value of key "Ravinder " is "Thakur"

val["Ravinder"]= "Singh"

print  (val["Ravinder"]) ## changed the value of dictionary


### only last value of key will be printed out when multiple times key name is same like Toward in below example ##

check = {"Toward": "Life", "India": "Rising", "Toward":"New Test"}

print check["Toward"]



#The Update() Method

dict1 = {'bookA': 1, 'bookB': 2, 'bookC': 3}
dict2 = {'bookC': 2, 'bookD': 4, 'bookE': 5}

dict1.update(dict2) ## merge two common value
print dict1

dict2.update(dict1)
print dict2

## Merging Two Dictionaries in a Single Expression
from itertools import chain
from collections import defaultdict
dict1 = {'bookA': 1, 'bookB': 2, 'bookC': 3}
dict2 = {'bookC': 2, 'bookD': 4, 'bookE': 5}
dict3 = defaultdict(list)
for k, v in chain(dict1.items(), dict2.items()):
    dict3[k].append(v)

for k, v in dict3.items():
    print(k, v)
