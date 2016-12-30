import os, re

directory = os.listdir('/Users/DrAbder/Desktop/Abder')
os.chdir('/Users/DrAbder/Desktop/Abder')

for file in directory:
    open_file = open(file,'r')
    read_file = open_file.read()
    regex = re.compile('Adber')
    read_file = regex.sub('Abder', read_file)
    write_file = open(file,'w')
    write_file.write(read_file)


###Compile a regular expression pattern into a regular expression object,
##which can be used for matching using its match()and search() methods.

regex = re.compile('Adber')
read_file = regex.sub('Abder', read_file) ## replace using sub regular expression and it will replace Adber to Abder


#out = re.search(r'^Rav*', ravi.txt)
#print out
