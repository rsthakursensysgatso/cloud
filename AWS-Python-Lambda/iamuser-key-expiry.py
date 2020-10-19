#!/usr/bin/python3.6

import boto3
import datetime


import datetime
import dateutil
import boto
from dateutil import parser
from boto import iam

conn=iam.connect_to_region('ap-southeast-1')
users=conn.get_all_users()
timeLimit=datetime.datetime.now() - datetime.timedelta(days=90)

ulist=[]
def username():

        for user in users.list_users_response.users:

            accessKeys=conn.get_all_access_keys(user_name=user['user_name'])

            for keysCreatedDate in accessKeys.list_access_keys_response.list_access_keys_result.access_key_metadata:

                if parser.parse(keysCreatedDate['create_date']).date() <= timeLimit.date():

                    ulist.append(user['user_name'])
        return ulist


uml=set(username())
#print(uml)


print('------List of username WHOS key is Older than 90 days')
for i in uml:
      print(i)
print('------List of username  End')

resource = boto3.resource('iam')
client = boto3.client("iam")

KEY = 'LastUsedDate'


for user in resource.users.all():
    Metadata = client.list_access_keys(UserName=user.user_name)
    for un in uml:
        if user.user_name ==  un:
            if Metadata['AccessKeyMetadata'] :
                for key in user.access_keys.all():
                    AccessId = key.access_key_id
                    Status = key.status
                    LastUsed = client.get_access_key_last_used(AccessKeyId=AccessId)
                    if (Status == "Active"):
                        if KEY in LastUsed['AccessKeyLastUsed']:
                            print("User: " , user.user_name ,  "Key: " , AccessId , "AK Last Used: " , LastUsed['AccessKeyLastUsed'][KEY])
                        else:
                            print("User: ", user.user_name  , "Key: ",  AccessId , "Key is Active but NEVER USED")
                    else:
                        print("User: ", user.user_name  , "Key: ",  AccessId , "Keys is InActive")
            else:
                print("User: ", user.user_name  , "No KEYS for this USER")   
