import sys
sys.path.append('rds-snapshot-cluster')
import boto3
import datetime

from subprocess import Popen, PIPE
import os
import subprocess
import json






def lambda_handler(event, context):
	global bkpmessage
	print("Connecting to RDS")
	client = boto3.client('rds')
	dbs = client.describe_db_clusters()
	for db in dbs['DBClusters']:
	        dbident=(db['DBClusterIdentifier'])
	        #print(dbident)
	        print("RDS  snapshot backups stated at %s...\n" % datetime.datetime.now())
	        try:
	                client.create_db_cluster_snapshot(
	                    DBClusterIdentifier=dbident,
	                    DBClusterSnapshotIdentifier='%s-%s' % (dbident, datetime.datetime.now().strftime("%y-%m-%d-%H-%M")),
	                    Tags=[
	                        {
	                            'Key': 'manual-snapshot',
	                            'Value': 'rdsbkp'
	                        },
	                    ]
	                )
	                bkpmessage= "Backup started & will Complete Soon for Database", dbident
	                pub()
	        except Exception as e:
	                        print('Cannot Create Snapshot Because Backup in progress or DB is not in available state '+ str(e))

	                        bkpmessage ='Cannot Create Snapshot Because Backup in progress or DB is not in available state', dbident
	                        pub()



	for db in dbs['DBClusters']:
	        dbidnt=(db['DBClusterIdentifier'])
	        for snapshot in client.describe_db_cluster_snapshots(DBClusterIdentifier=dbidnt, MaxRecords=50)['DBClusterSnapshots']:
	                if 'SnapshotCreateTime' in snapshot:
	                   create_ts = snapshot['SnapshotCreateTime'].replace(tzinfo=None)
	                   if create_ts < datetime.datetime.now() - datetime.timedelta(days=1):
	                        try:
	                                instance_arn = (snapshot['DBClusterSnapshotArn'])
	                                instance_tags = client.list_tags_for_resource(ResourceName=instance_arn)
	                                for i in instance_tags['TagList']:
	                                        if i['Value']=='rdsbkp':
	                                                bkpmessage="Deleting snapshots Older than 90 Days:", snapshot['DBClusterSnapshotIdentifier']
	                                                pub()
	                                                client.delete_db_cluster_snapshot(
	                                                    DBClusterSnapshotIdentifier=snapshot['DBClusterSnapshotIdentifier']
	                                                )
	                        except Exception as f:
	                                print('Cannot Delete Snapshot id '+ snapshot['DBClusterSnapshotIdentifier'])
	                                #bkpmessage = 'Cannot Delete Snapshot id because it is not old enough to delete'+ snapshot['DBClusterSnapshotIdentifier']
	                                #pub()

def pub():
    runslack = subprocess.Popen(["python3.6", "rds-snapshot-cluster/slack.py", str(bkpmessage)], stdout=subprocess.PIPE)
    out, err = runslack.communicate()
    print(out)
