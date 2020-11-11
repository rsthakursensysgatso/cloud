#!/usr/bin/python3.6

import boto3
f = open('snapshot-not-exist', 'r')
mylist = f.read().splitlines()

taglist=[]

def uniql():
	for i in mylist:
		#print(i)
		ec2 = boto3.client('ec2',  region_name='eu-west-1')
		image=ec2.describe_images(ImageIds=[i])
		for img in image['Images']:
        #print (img['ImageId'])
			for val in img['BlockDeviceMappings']:
				imd =img['ImageId']
				snap = val['Ebs']['SnapshotId']
				#for newv in val['Ebs']:
				print(newv['SnapshotId'])
				print("%s %s"% (imd, snap))
				#taglist.append(img['ImageId'])
	return taglist
uniql()
