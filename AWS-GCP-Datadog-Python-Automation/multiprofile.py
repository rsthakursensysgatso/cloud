#!/usr/bin/python3.6

import boto3
#import pytz
from datetime import datetime, timedelta


session = boto3.session.Session(profile_name='vantest')
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)


session = boto3.session.Session(profile_name='default')
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)

allprofile = boto3.session.Session().available_profiles
print(allprofile)
