import re
r'abc'
r'^abc'
r'abc$'
r'\$\d\d\.\d\d' ### $13.56 etcc..

r'\d\d\.\d\d'  ## This will be used for this for of digit 13.43

r'\d+\.\d+' or r'\d+\.\d\d' ## This pattern matches any of the below numberical
13.34
1.54
133.3
6.545
#+ one or More
#* Zero or More
#? zero or one
#{2,4} custom between 2 & 4

pattern = r'^\d+\.\d\d'
#pattern = r'^\w+\.\d'
test_str = [ '12.45',
             '56.55',
             '4.56',
             'dd.123.6444.',
             '65.9',
]

for my_str in test_str:
    if re.search(pattern, my_str):
        print '"%s" pattern matches "%s"' % (pattern, my_str)

#val = r'^a+b*c$'
val = r'a+x?b*x?c{1,3}x?'
chrr = [ 'aabcc',
         'dbccc',
         'abc',
         'accbbd'
         'abbccc'
         'axbxccx'
]

for i in chrr:
    if re.search(val, i):
        print '"%s" The value of "%s"' % (val, i)
    else:
        print '"%s" No Match value "%s"' % (val, i)
