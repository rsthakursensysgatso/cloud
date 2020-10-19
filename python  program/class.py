class Person:
    name = ''
    school = ''

    def print_name(self):
        print self.name

    def print_school(self):
        print self.school

abder = Person()
abder.name = 'Abder'
abder.school = 'XY University'
abder.print_name()
abder.print_school()


class Person:
    name = ''
    school = ''

    def print_information(self, name, school):
        print self.name
        print self.school

abder = Person()
abder.name = 'Abder'
abder.school = 'XY University'
abder.print_information(abder.name, abder.school)

## Class Person is created
class Person:
## self initiliazation  & initializing variables to default values
    def __init__(self, n, s):
        self.nam = n
        self.schol = s

    def print_name(self):
        print self.nam

    def print_school(self):
        print self.schol
  ## Instance and Object are same here object of class person is created named as abder
abder = Person('Abder', 'XY University')
abder.print_name()
abder.print_school()






class thakur:

    def __init__(self, var2, rav):
        self.var = var2
        self.var1 = rav
        print "The value of var2", self.var
        print "The value of var2", self.var1

    def che(self):
            print self.var

    def r(self):
            print self.var1

valll = thakur('Devops', 'Cloud')
valll.che()
valll.r()




class prod:
#tp = ('Devops', 'Rocks')
    def __init__(a,b,d):
        a.b = b
        a.d = d
    def val(a):
        print a.b
    def new(a):
        print a.d

out = prod('Python', 'Rocks')
#out = prod(tp)
out.val()
out.new()
#print "Check this value of object in the instance val", out.val()
#print "Check this value of object in the instance new", out.new()
