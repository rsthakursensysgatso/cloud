#!/usr/bin/python3.6

from datadog import initialize, api
import requests
import json
import re, os
from os import environ
import shutil
from gcloud import storage
import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=environ.get('BUCKET_POLICY')
now = datetime.date.today()
bucket='datadog-dashboard-test-bkp'
bucket_zip='datadog-dashboard-test-bkp.tar.{}.gz'.format(now)
print(bucket_zip)

options = {
}

initialize(**options)

APP_DATA = environ.get('DATA_KEY')

with open(APP_DATA, 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)
API_KEY = str(obj['api_key'])
APP_KEY = str(obj['app_key'])

r = \
    requests.get('https://api.datadoghq.eu/api/v1/dashboard'
                 , headers={'Content-Type': 'application/json',
                 'DD-API-KEY': '{}'.format(API_KEY),
                 'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})

mydict = {}
def mylist_func():
    for i in r.json()['dashboards']:
        mydict.update({i.get('title'): i.get('id')})
    print(mydict)
    return mydict

mylist_func()

os.makedirs("{}".format(bucket), exist_ok=True)

for k,v in mylist_func().items():
    r =requests.get('https://api.datadoghq.eu/api/v1/dashboard/{}'.format(v), headers={'Content-Type': 'application/json','DD-API-KEY': '{}'.format(API_KEY),'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})
    suffix = '.json'
    print(k)
    with open('{}/{}'.format(bucket, k) + suffix, 'w') as f:
        json.dump(r.json(), f, ensure_ascii=False)

os.system('tar -cvf datadog-dashboard-test-bkp.tar datadog-dashboard-test-bkp')
os.system('gzip datadog-dashboard-test-bkp.tar')
os.system('mv datadog-dashboard-test-bkp.tar.gz {}'.format(bucket_zip))

try:
    client = storage.Client()
    bucket = client.get_bucket('{}'.format(bucket))
    blob = bucket.blob(bucket_zip)
    print('Uploading {} file... to GCS bucket {}'.format(bucket_zip, bucket))
    blob.upload_from_filename(bucket_zip)
except Exception as e:
    print('Backup failed with error message'+ str(e))

