#!/usr/bin/python
import MySQLdb
db = MySQLdb.connect("localhost","whois","password","whois" )
cursor = db.cursor()

cxn = MySQLdb.connect(db='whois')
cur = cxn.cursor()

cur.execute('CREATE TABLE domain(Domain_Name varchar(30) NOT NULL,  Registrar varchar(30) NOT NULL,  Sponsoring_Registrar_IANA_ID varchar(40) NOT NULL,  Whois_Server varchar(40) NOT NULL,  Referral_URL varchar(30) NOT NULL, Name_Server varchar(100) NOT NULL,  Name_Server1 varchar(100) NOT NULL,  Status varchar(100) NOT NULL,  Updated_Date varchar(100) NOT NULL,  Creation_Date varchar(100) NOT NULL,  Expiration_Date varchar(100) NOT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1;')


cur.execute("INSERT INTO domain VALUES('POSTFIX.COM', 'Registrar: ENOM, INC.', 'Sponsoring Registrar IANA ID: 48', 'Whois Server: whois.enom.com', 'Referral URL: http://www.enom.com', 'Name Server: NS1.CLOUD9.NET', 'Name Server: NS2.CLOUD9.NET', 'Status: clientDeleteProhibited http://www.icann.org/epp#clientDeleteProhibited', 'Updated Date: 14-jul-2013', 'Creation Date: 19-jan-2000', 'Expiration Date: 19-jan-2017')")

cur.execute("INSERT INTO domain VALUES('CLOUD.COM', 'CSC CORPORATE DOMAINS, INC.', 'Sponsoring Registrar IANA ID: 299', 'Whois Server: whois.corporatedomains.com', 'Referral URL: http://www.cscglobal.com/global/web/csc/digital-brand-services.html', 'Name Server: NS-1310.AWSDNS-35.ORG', 'Name Server: NS-1736.AWSDNS-25.CO.UK', 'Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited', 'Updated Date: 03-feb-2016', 'Creation Date: 13-dec-2000', 'Expiration Date: 13-dec-2017')")

cur.execute("INSERT INTO domain VALUES('ITWORLD.COM', 'Registrar: MARKMONITOR INC.', 'Sponsoring Registrar IANA ID: 292', 'Whois Server: whois.markmonitor.com', 'Referral URL: http://www.markmonitor.com', 'Name Server: NS-1310.AWSDNS-35.ORG', 'Name Server: NS-A.PNAP.NET', 'Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited', 'Updated Date: 25-jan-2016', 'Creation Date: 27-feb-1998', 'Expiration Date: 26-feb-2017')")
