#!/usr/bin/python3.6

import json
import csv

download_dir = "findingsalert.csv"

csv = open(download_dir, "a") 
columnTitleRow = "serverity, value\n"


import sys
var1 = sys.argv[1]
var2 = json.loads(var1)


for key in var2.keys():
        for i in var2[key]:
                for k,v in i.items():
			if k == "recommendation":
				rec = v
			if k == "confidence":
				conf = v
			if k == "description":
				desc = v
                        if k == "severity":
                                sev = v

                        if k == "arn":
				arn = v
			if k == "indicatorOfCompromise":
				indicator = v
                        if k == "title":
                                title = v
                        if k == "numericSeverity":
				numericSeverity = v
			if k == "assetAttributes":
				for m,n in v.items():
					if m == "hostname":
						host = n
					if m == "autoScalingGroup":
						asg = n
					if m == "agentId":
						agentid = n
					if m == "amiId":
						amiid = n
					if m == "networkInterfaces":
						netinterfac = n[0]
						for q,w in netinterfac.items():
							if q == "privateIpAddresses":
								newv = w
								for vv in newv:
									for a,b in vv.items():
										if a == "privateIpAddress":
											pipaddr= b
									
			if k == "serviceAttributes":
				for o,p in v.items():
					if o == "rulesPackageArn":
						rulearn = p
					if o == "assessmentRunArn":
						assessarn = p
			if k == "updatedAt":
				updateat = v
			

			if k == "attributes":
				newk = v
				for i in newk:
					for s,r in i.items():
						print(r)
						if r == "CVSS3_SCORE":
							print(i["value"])
							CVSS3_SCORE = i["value"]
						if r == "CVSS3_VECTOR":
							print(i["value"])
							CVSS3_VECTOR = i["value"]
						if r == "CVSS2_VECTOR":
							print(i["value"])
							CVSS2_VECTOR = i["value"]
						if r == "CVSS2_SCORE":
							print(i["value"])
							CVSS2_SCORE = i["value"]
				
					
                row = str(CVSS3_SCORE) + ","  + str(CVSS3_VECTOR) + ","  + str(CVSS2_VECTOR) + ","  + str(CVSS2_SCORE) + ","  + str(updateat)  + ","  + str(conf)  + ","  + str(indicator) + ","  + str(numericSeverity) + ","  + pipaddr + ","  +   sev + ","  +   arn + "," + desc + "," + rec + "," + title + "," + host + "," + asg + "," + agentid + "," + amiid + rulearn + "," + assessarn +   "\n"
                csv.write(row)
