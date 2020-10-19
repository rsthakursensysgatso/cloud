#!/usr/bin/python

import sys

sys.stdout.write('Devops Cloud\n')
sys.stderr.flush()
sys.stdout.write('Next write ready\n')

print (sys.argv)

if len(sys.argv) > 3:
    print "The value of second argument is", sys.argv[1]
else:
    print "Total length", len(sys.argv)
    print "The value of first argument is ", sys.argv[2]

## Now to do the sum with the total number of argument

if len(sys.argv) < 1:
    ssum = len(sys.argv) + 5
    print "Fist argument", sys.argv[1]
    print "The sume of less than one argument is ", ssum
else:
    osm = int(sys.argv[2]) + 10
    print osm
    print "The sum is different here that is ", osm
