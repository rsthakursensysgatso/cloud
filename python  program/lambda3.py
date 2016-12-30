print (lambda x, y: x*y)(3, 4)


ravi = lambda x,y,z: x + y +z
print ravi(4,56,34)

## OR WE CAN DEFINE LAMBDA IN ONE LINE

print (lambda x,y: x ** y)(20,2)

list = [1,4,5,6]
b = map(lambda x: x**2, list) ## each element from list will go to x and  power square action will be performed
print b

## OR ABOVE TASK WE CAN DO BY
#list = [1,4,5,6]
print map(lambda x: x*2, list) #### each value of element will be multiply with 2

state = ["Ravinder","Thakur","Devops"]
print map(lambda x = []: x, (state)) ## for each value of state it will return output as state only


print map(lambda  x: len(x), (state)) ## length of each element in list

print map(lambda x = (): x, (state)) ## each value of list is stored in the tuple

#print map(lambda)
