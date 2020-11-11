#!/usr/bin/python3.6

import boto3

def cred():
	ssm = boto3.client('ssm')
	parameter = ssm.get_parameter(Name='rabbitmq',  WithDecryption=True)
	keyvalue = parameter['Parameter']['Value']
	#print(keyvalue)
	return print(keyvalue)
cred()
