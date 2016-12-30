
import re
ptr = r'(\d+)$'  ## String END with digit
prtr = r'^(\d+)' ## String start with number
prtr = r'(\d+)' ## Print only string out of mix of char & integer string like 54EE it will retrn 54 only
val1 = r'(\d+)+[A-Z]' ## Retunr element start with number and end with Alpahbet 51D, 33367E etcc
val2 = r'([a-z]+)(\d+)' #### Return element start with Alpahbet & end with number that is A22
char = r'(\d+)'
test_str = ['ravinder',
            '1983',
            'house',
            'Number',
            'Sector',
            '51d',
            '3367E',
            'a22',
            'chandigarh',
            'jakarta',
            'devops $#@#%'
           ]
#pt = r'(\w+)'
#for i in test_str:
for i in test_str:
    chk = re.search(val2, i)
    #print chk.group(0)
    if chk:
        #print chk[0]
        #Below two groups will create one for patter ([a-z]+) and second (\d+)
        (letters, digits) = chk.groups()
        print "letter %s,  digit %s" %(letters, digits)
        #print (letter {0},  digit {1}).format(letters, digits)



a = "Rav"
b = "inder"

out = a + b

print out

list = [how,are,you]
