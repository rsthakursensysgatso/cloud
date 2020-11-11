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
        'ToAddresses': ['ravinder.thakur@altusgroup.com', 'devopsteam@argussoftware.com'],
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
            'Data': 'AOD Prod Environment User Authentication Attempt Failure',
        },
    },
    Source='ravinder.thakur@altusgroup.com',
)
                                                
def cloudtrail(event, context):
	endtime = datetime.datetime.now()
	interval = datetime.timedelta(minutes=2000)
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
	print(result)
	for i in result:
		global username
		username = i['Username']
		varr = i['CloudTrailEvent']
		if "Failed authentication" or "No username found in supplied account"  in varr:
			global result1
			global result2
			ipaddr = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", varr)
			accountid = re.search(r"(\d+\d+?\d+\d+)", varr)
			result1 = ipaddr.group(0)
			result2 = accountid.group(0)
			print('calling send_alert_function')
			send_alert()
