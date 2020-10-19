import sys
sys.path.append('rabbitmq')
import os
import subprocess
import json
import boto3

def lambda_handler(event, context):
    
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='rabbitmq',  WithDecryption=True)
    keyvalue = parameter['Parameter']['Value']
    print(keyvalue)
    
    
    p = subprocess.Popen(["python3.6", "rabbitmq/rabbitmqadmin.py", "--host=duckbill.rmq.cloudamqp.com", "--port=443", "--ssl", "--vhost=lewsupnp", "--username=lewsupnp", "--password=" "%s" % keyvalue, "get", "queue=devops-testing-error", "count=300", "--depth=3"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    print(out)

    
    runslack = subprocess.Popen(["python3.6", "rabbitmq/slack.py", out], stdout=subprocess.PIPE)
    out, err = runslack.communicate()
    print(out)

    v = subprocess.Popen(["rabbitmq/shovel.sh"], stdout=subprocess.PIPE)
    out, err = v.communicate()
    print(out)

