list = [1,4,5,6]
b = map(lambda x: x**2, list) ## each element from list will go to x and  power square action will be performed
print b
a = map(lambda x: x * 10, range(20)) ## each element from range 0 to 20 will go to x and 10 will multiply
print a


#d = map(def a(var))

def a(var):
    for i in var:
        b = 10
        c =  b + i
        print c
        return c
print a(range(5))
