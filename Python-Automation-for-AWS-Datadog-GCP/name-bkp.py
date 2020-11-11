#!/usr/bin/python3.6


import re
import boto3
import datetime
from botocore.config import Config


# Get a list of all AMIs owned by this account_id

config = Config(
    retries = dict(
        max_attempts = 10
    )
)

client = boto3.client('ec2', region_name='eu-west-1', config=config)

def delimage():
	ami_filter = [{"Name": "tag:ravi", 'Values': ["ami-ready-to-delete"]}]
#response = client.describe_images(Filters=ami_filter, Owners=['self'])
	response = client.describe_images(Filters=ami_filter)
	for ami in response['Images']:
		#imageid= ami['ImageId'])  # Or whatever you wish to do
		#imagename= ami['aminame']
		name = ami['Name']
		imageid= ami['ImageId']
		print('Image deleted as part of clean up space NAME {}  IMAGE ID  {}'.format(name, imageid))

delimage()
