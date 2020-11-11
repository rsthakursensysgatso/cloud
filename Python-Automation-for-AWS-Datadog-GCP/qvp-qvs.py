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


qvsimage=[]
def mown():
#	ami_filter = [{"Name": "tag:ravi", 'Values': ["ami-do-not-delete"]}]
	ami_filter = [{"Name": "tag:ravi", 'Values': ["ami-ready-to-delete"]}]
	own = client.describe_images(Owners=['985988425364'], Filters=ami_filter)
	for i in own['Images']:
		#print(i['ImageId'])
		qvsimage.append(i['ImageId'])
	return qvsimage

#mown()
#private()

ec2 = boto3.resource('ec2')

img=mown()
for i in img:
	response = client.describe_images(ImageIds=[i])
	for s in response['Images']:
		#snapid = s['BlockDeviceMappings']['Ebs']
		for n in s['BlockDeviceMappings']:
			try:
				print(n['Ebs']['SnapshotId'])
				client.create_tags(Resources=[n['Ebs']['SnapshotId']], Tags=[{'Key': 'ravi', 'Value': 'snapshot-ready-to-delete'},])
			except Exception as e:
			        print('Snapshot Device is ephemeral'+ str(e))
			#print(n)
#			for i in n['Ebs']:
			#print(n['Ebs'])
#				print(n['SnapshotId'])
			#client.create_tags(Resources=[n['Ebs']['SnapshotId']], Tags=[{'Key': 'ravi', 'Value': 'snapshot-ready-to-delete'},])
#			for o in n['Ebs']:
#				print(o['SnapshotId'])
			
			
		
#		r p in s['BlockDeviceMappings']:
#			print(p['SnapshotId'])
#			print('QMS or QVP Snapshot  id {}'.format(p['SnapshotId']))
                        #image = ec2.Image(imageid)
                        #image.create_tags(Tags=[{'Key': 'ravi', 'Value': 'ami-do-not-delete'},])
