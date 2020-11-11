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

def private():
	ami_filter = [{"Name": "is-public", 'Values': ["false"]}]
#response = client.describe_images(Filters=ami_filter, Owners=['self'])
	response = client.describe_images(Filters=ami_filter)
	for ami in response['Images']:
		print(ami['ImageId'])  # Or whatever you wish to do


def mown():
	own = client.describe_images(Owners=['985988425364'])
	for i in own['Images']:
		print(i['ImageId'])

#mown()
#private()

ec2 = boto3.resource('ec2')

#f = open('/tmp/testami', 'r')
f = open('alluseduniqami', 'r')
used = f.read().splitlines()

u = open('alluniqami', 'r')
#u = open('/tmp/finalused-test', 'r')
uniq = u.read().splitlines()

for i in uniq:
	if i not in used:
		#print(i)

			try:
		                response = client.describe_images(ImageIds=[i])
		                for s in response['Images']:
		                        create_date = s['CreationDate']
		                        imageid = s['ImageId']
		                        qview = s['Name']
		                        datevar = ['2015','2015']
		                        patrn = re.search("201[5-5]", create_date)
		                        patrn2 = re.search("Q[VM]+", qview)
		                        patrn3 = re.search("qlikview", qview)
		                        if patrn and patrn2:
		                                try:
		                                        print('QMS or QVP image id {}'.format(imageid))
		                                        image = ec2.Image(imageid)
		                                        image.create_tags(Tags=[{'Key': 'ravi', 'Value': 'ami-do-not-delete'},])
		                                except Exception as e:
		                                        print('Tag not possible for QVS or QVP AMI'+ str(e))
		                        elif patrn and patrn3:
		                                try:
		                                        print('qlikview  image id {}'.format(imageid))
		                                        image = ec2.Image(imageid)
		                                        image.create_tags(Tags=[{'Key': 'ravi', 'Value': 'ami-do-not-delete'},])
		                                except Exception as f:
		                                        print('Tag not possible for QVS or QVP AMI'+ str(f))

		                        elif patrn and not patrn2 and not patrn3:
		                                try:
		                                        print('Tagging 2015 & 2015 IMAGE AMI {} which can be removed'.format(imageid))
		                                        image = ec2.Image(imageid)
		                                        image.create_tags(Tags=[{'Key': 'ravi', 'Value': 'ami-ready-to-delete'},])
		                                except Exception as m:
		                                        print('Tag not possible for AMI'+ str(m))
		                        else:
		                                print('Not Tagged AMI {} Outside 2015 & 2015'.format(imageid))

			except Exception as imnotex:
				print('Image not exist  AMI'+ str(imnotex))
