#!/usr/bin/python3.6

import boto3
import datetime

from subprocess import Popen, PIPE
import os
import subprocess
import json



def pub():
    runslack = subprocess.Popen(["python3.6", "rds/slack.py", str(bkpmessage)], stdout=subprocess.PIPE)
    out, err = runslack.communicate()
    print(out)



def lambda_handler(event, context):

	print("Connecting to RDS")
	client = boto3.client('rds')
	dbs = client.describe_db_clusters()

	for db in dbs['DBClusters']:
#	        dbident=(db['DBClusterIdentifier'])
	        dbident="newstagedb-cluster"
	        print(dbident)
	        print("RDS  snapshot backups stated at %s...\n" % datetime.datetime.now())
	        try:
	                client.create_db_cluster_snapshot(
	                    DBClusterIdentifier=dbident,
	                    DBClusterSnapshotIdentifier='%s-%s' % (dbident, datetime.datetime.now().strftime("%y-%m-%d-%H-%M")),
	                    Tags=[
	                        {
	                            'Key': 'CostCenter',
	                            'Value': 'rdsbkp'
	                        },
	                    ]
	                )
	                bkpmessage= "Backup started & will Complete Soon for Database", db['DBClusterIdentifier']
	                pub()
	        except Exception as e:
	                        print('Cannot Create Snapshot Because Backup in progress or DB is not in available state '+ str(e))

	                        bkpmessage = 'Cannot Create Snapshot Because Backup in progress or DB is not in available state', db['DBInstanceIdentifier']
	                        pub()

	for db in dbs['DBClusters']:
#	        dbidnt=(db['DBClusterIdentifier'])
	        dbidnt="newstagedb-cluster"
	        for snapshot in client.describe_db_cluster_snapshots(DBClusterIdentifier=dbidnt, MaxRecords=50)['DBClusterSnapshots']:
	                if 'SnapshotCreateTime' in snapshot:
	                   create_ts = snapshot['SnapshotCreateTime'].replace(tzinfo=None)
	                   if create_ts < datetime.datetime.now() - datetime.timedelta(days=7):
	                        try:
	                                instance_arn = (snapshot['DBSnapshotArn'])
	                                instance_tags = client.list_tags_for_resource(ResourceName=instance_arn)
	                                for i in instance_tags['TagList']:
	                                        if i['Value']=='rdsbkp':
	                                                bkpmessage= "Deleting snapshots Older than 90 Days:", snapshot['DBClusterSnapshotIdentifier']
	                                                pub()
	                                                client.delete_db_snapshot(
	                                                    DBSnapshotIdentifier=snapshot['DBClusterSnapshotIdentifier']
	                                                )
	                        except Exception as f:
	                                print('Cannot Delete Snapshot id '+ str(f))
	                                bkpmessage = 'Cannot Delete Snapshot id '+ str(f)
	                                pub()
