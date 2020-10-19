
names = ["Michele", "Robin", "Sara", "Michele", "Test", "Test"]
names = set(names)  ###a set is a collection of elements where no element is repeated.
names = list(names)
print names

a_list = ["Ravinder", "Singh", "Thakur", "Devops"]

def list_en(a_list):
    #return [a_list[0], a_list[len(a_list)-1]]
    print [a_list[0:2]]
list_en(a_list)
