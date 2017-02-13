#!/usr/bin/python
import MySQLdb
import sys

db = MySQLdb.connect("localhost","whois","password","whois" )
cursor = db.cursor()

sql = "select * from domain"
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
 if row[0] == sys.argv[1]:
    print row[0]
    print row[1]
    print row[2]
    print row[3]
    print row[4]
    print row[5]
    print row[6]
    print row[7]
    print row[8]
    print row[9]
    print row[10]
tdel=[]
for row in results:
  res=row[0]
  tdel.append(res)
  out=len(tdel)
print "Domain Name Exist in Database", tdel
print "Total number of domain name in Database", out

db.close()
