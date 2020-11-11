from __future__ import print_function

import json

import boto3
import urllib.request
import time

print('Loading function')


def lambda_handler(event, context):
    ssm_client = boto3.client('ssm', region_name="eu-west-1")
    params={"commands":["ipconfig"]}
    #params={"commands":["C:\\Users\\Administrator\\Desktop\\S3-DM-Update.ps1"]}
    response = ssm_client.send_command(
            InstanceIds=['i-0d03d6a501d651d4e'],
            DocumentName='AWS-RunPowerShellScript',
            Parameters=params
            )
    command_id = response['Command']['CommandId']
    time.sleep(2) 
    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId='i-0d03d6a501d651d4e',
        )
    print(output)
