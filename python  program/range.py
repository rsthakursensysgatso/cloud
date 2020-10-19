a = range(2,10)
print a

b = a
b = []

for i in a:
    print i*2

## Append operation

c = [] ## listt
#d = () ## tuple

for i in a:
    c.append(i*2)
    print c

## other way to double rather than for loop is

#[map (double, a)]

### check whether the number is even
a = range(10,16)
def is_even(a):
    return x % 4 == 0
    is_even(2)

# whether the fucntion even to check it
#filter[is_even, a]

#reduce(sum, a)

#for i in a:
    #print [a for a in i]
