#!/usr/bin/python
import MySQLdb
db = MySQLdb.connect("localhost","whois","password","whois" )
cursor = db.cursor()

cxn = MySQLdb.connect(db='whois')
cur = cxn.cursor()

cur.execute('CREATE TABLE domain(Domain_Name varchar(30) NOT NULL,  Registrar varchar(30) NOT NULL,  Sponsoring_Registrar_IANA_ID varchar(40) NOT NULL,  Whois_Server varchar(40) NOT NULL,  Referral_URL varchar(30) NOT NULL, Name_Server varchar(100) NOT NULL,  Name_Server1 varchar(100) NOT NULL,  Status varchar(100) NOT NULL,  Updated_Date varchar(100) NOT NULL,  Creation_Date varchar(100) NOT NULL,  Expiration_Date varchar(100) NOT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1;')

