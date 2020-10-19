import os
print(os.getcwd())## Current working directory

print(os.listdir("."))  ## to present all the file and directory in curent working Directory

cwd = os.getcwd()

files = os.listdir(cwd)
print "THe abosute path"
print (files) ## list  all the files in current working directory
for fil in files:
    path = os.path.join(cwd, fil) ## file path append by join function with current working directory
    print (path)

var = "E:\python\python in hindi\python own program\ravi.txt"
cwd = os.getcwd()
lis = os.listdir(cwd)
for fil in lis:
    #out = os.listdir(fil)
    #print (fil)
    #path = os.path.join(cwd, fil)
    if fil == "ravi.txt":
        print "Got it"
#        print (out)



for dirpath, dirnames, files in os.walk(cwd):
    for file in files:
        print(os.path.join(dirpath, file))

walk = os.walk(cwd)
print (walk)
