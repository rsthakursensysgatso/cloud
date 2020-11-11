#!/usr/bin/python3.6

import boto3
import datetime

#client = boto3.client('ec2')
client = boto3.client('ec2', 'eu-west-1')
def snapshot():
	val = volid()
	#print(type(val))
	for i in val:
		snapshot= client.describe_snapshots(
			Filters=[
			{
			'Name': 'volume-id',
			'Values': [
				i,
				]
				},
				]
				)
		for s in snapshot['Snapshots']:
			print(s['SnapshotId'],s['VolumeId'],s['StartTime'])


def volid():
        volumeid=[]
        ec2instance = client.describe_instances()
        for s in ec2instance['Reservations']:
                for i in s['Instances']:
                        for ni in  i['BlockDeviceMappings']:
                                volumeid.append(ni['Ebs']['VolumeId'])
        return volumeid
snapshot()
