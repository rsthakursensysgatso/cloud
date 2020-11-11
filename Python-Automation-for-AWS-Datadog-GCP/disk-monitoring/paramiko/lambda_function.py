import sys
sys.path.append('paramiko')
import os
import subprocess
import boto3



#filters = [{'Name': 'tag:Name', 'Values': ['taggingserver']},{'Name':'instance-state-name', 'Values':['running']}] 
filters = [{'Name': 'tag:instancevpc', 'Values': ['vpc-63cd2406']},{'Name':'instance-state-name', 'Values':['running']}]

instdict = {}
finallist = {}


def lambda_handler(event, context):
        val = ec2list()
        global k
        global v
        global keyvalue
        #print(type(val))
        for k,v in val.items():
            ssm = boto3.client('ssm')
            parameter = ssm.get_parameter(Name=v,  WithDecryption=True)
            keyvalue = parameter['Parameter']['Value']
            finallist[k]=keyvalue
            #print(finallist)
        return finallist
            


def ec2list():
        instancelist = []
        ec2 = boto3.client('ec2')
        response = ec2.describe_instances(Filters=filters)
        global serverkeyname
        for r in response['Reservations']:
                for i in r['Instances']:
                        serverkeyname = i['KeyName']
                        #print(serverkeyname)
                        pipadd=i['PrivateIpAddress']
                        instancelist.append(i['PrivateIpAddress'])
                        instdict[i['PrivateIpAddress']] = i['KeyName']
        return instdict



