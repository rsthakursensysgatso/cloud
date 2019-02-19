import sys
sys.path.append('appd')
import os
import requests
import json
import boto3

usr="ravinder.thakur@testaccount.com@testgroup"
url="https://testaccount.saas.appdynamics.com/controller/rest/applications/qa-test-platform/problems/healthrule-violations?output=json&time-range-type=BEFORE_NOW&duration-in-mins=15"


	
def password():
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name='appdloginpasswd',  WithDecryption=True)
        keyvalue = parameter['Parameter']['Value']
        return str(keyvalue)

password()
mypwd=password()
response = requests.get(url, auth=(usr, mypwd))
val = response.status_code
json = response.json()

qanodeid=[]
def qanode():
	for i in json:
		qanodeid.append(i['affectedEntityDefinition']['entityId'])
		
	return qanodeid

def qaremovenode():
	qanodelist=qanode()
	print(qanodelist)
	for val in qanodelist:
		r = requests.post("https://testaccount.saas.appdynamics.com/controller/rest/mark-nodes-historical?application-component-node-ids={}".format(val), auth=(usr, mypwd))
		print(r.status_code)

testurl="https://testaccount.saas.appdynamics.com/controller/rest/applications/testtest-test-platform/problems/healthrule-violations?output=json&time-range-type=BEFORE_NOW&duration-in-mins=15"

testresponse = requests.get(testurl, auth=(usr, mypwd))
testjson = testresponse.json()

testnodeid=[]
def testnode():
        for i in testjson:
                testnodeid.append(i['affectedEntityDefinition']['entityId'])

        return testnodeid

def testremovenode():
        testnodelist=testnode()
        print(testnodelist)
        for val in testnodelist:
                r = requests.post("https://testaccount.saas.appdynamics.com/controller/rest/mark-nodes-historical?application-component-node-ids={}".format(val), auth=(usr, mypwd))
                print(r.status_code)

def purgenode(event, context):
	testremovenode()
	qaremovenode()
