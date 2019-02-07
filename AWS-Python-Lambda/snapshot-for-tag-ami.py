#!/usr/bin/python3.6

import re
import boto3
from botocore.config import Config


config = Config(
    retries = dict(
        max_attempts = 10
    )
)


taglist=[]
def list_ami():
	filters = [{'Name': 'tag:ravi', 'Values': ['ami-for-deletion']}
	]

	ec2 = boto3.client('ec2',  region_name='eu-west-1', config=config)
	image=ec2.describe_images(Filters=filters)
	for img in image['Images']:
		#print(img)
		try:
			for val in img['BlockDeviceMappings']:
				imd =img['ImageId']
				snap = val['Ebs']['SnapshotId']
				print("%s %s"% (imd, snap))
		except Exception as e:
			print('Snapshot does not exist for ami %s'% imd)

		#taglist.append(img['ImageId'])

list_ami()
#list_ami()


f = open('snapshot-not-exist', 'r')
mylist = f.read().splitlines()

#for i in mylist:
#	print(i)

