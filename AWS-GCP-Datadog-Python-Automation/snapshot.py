#!/usr/bin/python3.6

import boto3
import datetime

#today = datetime.now() + timedelta(days=1)
#two_weeks = timedelta(days=14) 
#start_date = today - two_weeks

age = 1900



#client = boto3.client('ec2')
client = boto3.client('ec2', 'eu-west-1')

def days_old(date):
    date_obj = date.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

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
#			StartTime=start_date
			#EndTime=today
				)
		for s in snapshot['Snapshots']:
#			print(s['SnapshotId'],s['VolumeId'],s['StartTime'])
			create_date = s['StartTime']
			snapshot_id = s['SnapshotId']
			day_old = days_old(create_date)
			if day_old > age:
				print(snapshot_id)
 


def volid():
        volumeid=[]
        ec2instance = client.describe_instances()
        for s in ec2instance['Reservations']:
                for i in s['Instances']:
                        for ni in  i['BlockDeviceMappings']:
                                volumeid.append(ni['Ebs']['VolumeId'])
        return volumeid
snapshot()
