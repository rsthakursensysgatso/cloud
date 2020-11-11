import sys
sys.path.append('rds-snapshot')

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
    dbs = client.describe_db_instances()

    for db in dbs['DBInstances']:
            dbident=(db['DBInstanceIdentifier'])
            print("RDS  snapshot backups stated at %s...\n" % datetime.datetime.now())
            response = client.list_tags_for_resource(ResourceName=db['DBInstanceArn'])
            for i in response['TagList']:
                if i.get('Value') == 'backup' and i.get('Key') == 'manual-snapshot':
                    
                    try:
                        
                                client.create_db_snapshot(
                                    DBInstanceIdentifier=dbident,
                                    DBSnapshotIdentifier='%s-%s' % (dbident, datetime.datetime.now().strftime("%y-%m-%d-%H-%M")),
                                    Tags=[
                                        {
                                            'Key': 'manual-snapshot',
                                            'Value': 'rdsbkp'
                                        },
                                    ]
                                )
                                bkpmessage= "Backup started & will Complete Soon for Database", db['DBInstanceIdentifier']
                                pub()
                    except Exception as e:
                                    print('Cannot Create Snapshot Because Backup in progress or DB is not in available state OR ITS Cluster RDS Instance'+ str(e))
        
                                    bkpmessage = 'Cannot Create Snapshot Because Backup in progress or DB is not in available state OR ITS Cluster RDS Instance', db['DBInstanceIdentifier']
                                    pub()

    for db in dbs['DBInstances']:
            dbidnt=(db['DBInstanceIdentifier'])
            for snapshot in client.describe_db_snapshots(DBInstanceIdentifier=dbidnt, MaxRecords=50)['DBSnapshots']:
                    if 'SnapshotCreateTime' in snapshot:
                       create_ts = snapshot['SnapshotCreateTime'].replace(tzinfo=None)
                       if create_ts < datetime.datetime.now() - datetime.timedelta(days=90):
                            try:
                                    instance_arn = (snapshot['DBSnapshotArn'])
                                    instance_tags = client.list_tags_for_resource(ResourceName=instance_arn)
                                    for i in instance_tags['TagList']:
                                            if i['Value']=='rdsbkp':
                                                    bkpmessage= "Deleting snapshots Older than 90 Days:", snapshot['DBSnapshotIdentifier']
                                                    pub()
                                                    client.delete_db_snapshot(
                                                        DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier']
                                                    )
                            except Exception as f:
                                    print('Cannot Delete Snapshot id '+ snapshot['DBSnapshotIdentifier'])
                                    #bkpmessage = 'Cannot Delete Snapshot id '+ str(f)
                                    #pub()



def pub():
    runslack = subprocess.Popen(["python3.6", "rds-snapshot/slack.py", str(bkpmessage)], stdout=subprocess.PIPE)
    out, err = runslack.communicate()
    print(out)

