import sys
sys.path.append('cloudtrail')
import boto3
import datetime  
from datetime import timedelta, datetime, tzinfo
import datetime
import re

ct_client = boto3.client('cloudtrail', region_name='us-east-1')

import boto3
AWS_REGION = "eu-west-1"

client = boto3.client(
    'ses',
    region_name=AWS_REGION)

def send_alert():
    response = client.send_email(
    Destination={
        'ToAddresses': ['ravinder.thakur@altusgroup.com', 'ravinder.thakur@altusgroup.com'],
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data':  "Account ID: -> " + result2 + "\n" + "IPAddress: -> " + result1 + "\n" + "Username: -> " + username,
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Below User Try to Access AWS Account',
        },
    },
    Source='ravinder.thakur@altusgroup.com',
)
                                                
def cloudtrail(event, context):
	endtime = datetime.datetime.now()
	interval = datetime.timedelta(minutes=5)
	starttime = endtime - interval
	response = ct_client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'EventName',
            'AttributeValue': 'ConsoleLogin'
        },
    ],
    StartTime=starttime,
    EndTime=endtime,
    MaxResults=20
)
	result = response['Events']
	print('Startttttttt')
	print(result)
	print('Enddddddddd')
	print('Second Startttttttt')
	for i in result:
		global username
		username = i['Username']
		varr = i['CloudTrailEvent']
		print(type(varr))
		print(varr)
		if "Failed authentication"  in varr:
			global result1
			global result2
			ipaddr = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", varr)
			accountid = re.search(r"(\d+\d+?\d+\d+)", varr)
			result1 = ipaddr.group(0)
			result2 = accountid.group(0)
			print(i['Username'])
			print(result1)
			print(result2)
			print('calling send_alert_function')
			send_alert()
