#!/usr/bin/python3.6

import boto3
#import pytz
from datetime import datetime, timedelta
import re
from botocore.config import Config

from subprocess import Popen, PIPE
import os
import subprocess


config = Config(
    retries = dict(
        max_attempts = 10
    )
)


def pub():
    runslack = subprocess.Popen(["python3.6", "slack.py", str(fsnap)], stdout=subprocess.PIPE)
    out, err = runslack.communicate()
    print(out)


client = boto3.client('ec2', region_name='eu-west-1', config=config)
ec2 = boto3.resource('ec2', region_name='eu-west-1', config=config)
volume_iterator = ec2.volumes.all()

########### ALL VOLUME SNAPSHOT ID ##############
avid=[]
response = client.describe_volumes()
for i in response['Volumes']:
        avid.append(i['SnapshotId'])
print(len(avid))
print(avid)


owner='878723232412'      
snapshots  = client.describe_snapshots(OwnerIds=[owner])
snapshot_list=snapshots['Snapshots']
############ ALL SNAPSTHOTS AMI ID #####################
allamilist=[]
for i in snapshot_list:
	try:
		newi = re.search(r'ami-[a-z0-9]+', i['Description'])
		amid = newi.group(0)
		if amid:
			allamilist.append(amid)
		else:
			print('AMI NOT STARTED WITH AMI')
	except Exception as f:
		print('AMI Description Name doesnot Start  ami-'+ i['Description'])


################ ALL PRIVATE AMI ID LIST ###############
pimg=[]
ami_filter = [{"Name": "is-public", 'Values': ["false"]}]
response = client.describe_images(Filters=ami_filter)
for ami in response['Images']:
	pimg.append(ami["ImageId"])


############ ALL AMI WHICH DO NOT EXIST IN ACCOUNT  AND DEREGISTER/DELETED ALREADY #########
noamisnap=[]
for i in allamilist:
	if i not in pimg:
		noamisnap.append(i)

print(len(noamisnap))


############## FILTER SNAPSHOTS WHICH BELONGS TO ALREADY DEREGISTER/DELETED AMI'S

finalsnap=[]
for i in snapshot_list:
	try:
		fnd  = re.search(r'ami-[a-z0-9]+', i['Description'])
		snap = fnd.group(0)
		if snap in noamisnap:
			#finalsnap.append(snap)
			finalsnap.append(i['SnapshotId'])
	except Exception as r:
		print('AMI Description Name doesnot Start  ami-'+ i['Description'])
print(len(finalsnap))


############ FINAL SNAPSHOT FILETER ===> TO REMOVE SNAPSHOT FROM IN Use/Available VOLUMES
fsnap=[]
for u in finalsnap:
	if u not in avid:
		fsnap.append(u)
print(fsnap)
pub()

for i in fsnap:
	try:
		print('Deleting Snapshot \t'+ i)
		client.delete_snapshot(SnapshotId=i)
	except Exception as dl:
		print('Cannot Delete snapshot \t'+ i)
