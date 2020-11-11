#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from datadog import initialize, api
import requests
import json
import re
from os import environ


APP_DATA = environ.get('DATA_KEY')

with open(APP_DATA, 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)
API_KEY = str(obj['api_key'])
APP_KEY = str(obj['app_key'])

timeperiod = "1600179893"
layout_type = 'ordered'
description = 'A dashboard with ANPR Policy Time'
is_read_only = True
notify_list = ['sdfd@test.com']
layout_type1 = 'ordered'
description1 = 'A dashboard with Condition Time'
is_read_only1 = True
notify_list1 = ['sdfd@test.com']


r = \
    requests.get('https://api.datadoghq.eu/api/v1/metrics?from={}'.format(timeperiod)
                 , headers={'Content-Type': 'application/json',
                 'DD-API-KEY': '{}'.format(API_KEY),
                 'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})
print('https://api.datadoghq.eu/api/v1/metrics?from={}'.format(timeperiod))

anpr_list = []
def anpr_func():
    for i in r.json()['metrics']:
        if re.search("\w+ANPR\w+Time.(avg)$", i):
            anpr_list.append(i)
    return anpr_list


policy_apply_list = []
def policy_func():
    for j in r.json()['metrics']:
        if re.search("Policy_Apply_Time_[a-zA-Z0-9]+.(avg)$", j):
            policy_apply_list.append(j)
    return policy_apply_list


cond_apply_list = []
def cond_func():
    for j in r.json()['metrics']:
        if re.search("Condition_Apply_Time_[a-zA-Z0-9]+.(avg)$", j):
            cond_apply_list.append(j)
    return cond_apply_list


options = {'api_host': 'https://api.datadoghq.eu/',
           'api_key': '{}'.format(API_KEY),
           'app_key': '{}'.format(APP_KEY)}

initialize(**options)

updated_list = []
def anpr_ll():
    for i in anpr_func():
        updated_list.append({'q': '{}{}'.format(i, '{*}')})
    return updated_list


policy_list = []
def policy_ll():
    for j in policy_func():
        policy_list.append({'q': '{}{}'.format(j, '{*}')})
    return policy_list


cond_list = []
def cond_ll():
    for j in cond_func():
        cond_list.append({'q': '{}{}'.format(j, '{*}')})
    return cond_list


try:
    def get_dashid():
        resp = requests.get('https://api.datadoghq.eu/api/v1/dashboard'
                            ,
                            headers={'Content-Type': 'application/json'
                            , 'DD-API-KEY': '{}'.format(API_KEY),
                            'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})
        for dic in resp.json()['dashboards']:
            for (k, v) in dic.items():
                if  re.search('demo-anpr-policy-time', str(v)):
                    return dic.get('id')
    requests.ddemote('https://api.datadoghq.eu/api/v1/dashboard/{}'.format(get_dashid()),
                    headers={'Content-Type': 'application/json',
                    'DD-API-KEY': '{}'.format(API_KEY),
                    'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})
    print('Ddemoting old Dashboard for ANPR policy Time')
except Exception as e:
    print('Dashboard does not exist so cannot ddemote')

print('Creating New Dashboard for ANPR Policy Time')
title = 'DEMO ANPR Policy Time'
widgets = [{'definition': {'type': 'timeseries', 'requests': anpr_ll(),
           'title': 'ANPR Policy'}},
           {'definition': {'type': 'timeseries',
           'requests': policy_ll(), 'title': 'Policy Apply Time'}}]


api.Dashboard.create(
    title=title,
    widgets=widgets,
    layout_type=layout_type,
    description=description,
    is_read_only=is_read_only,
    notify_list=notify_list,
    )

try:
    def get_dashid1():
        resp = requests.get('https://api.datadoghq.eu/api/v1/dashboard'
                            ,
                            headers={'Content-Type': 'application/json'
                            , 'DD-API-KEY': '{}'.format(API_KEY),
                            'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})
        for dic in resp.json()['dashboards']:
            for (k, v) in dic.items():
                if re.search('demo-condition-time', str(v)):
                    return dic.get('id')
    requests.ddemote('https://api.datadoghq.eu/api/v1/dashboard/{}'.format(get_dashid1()),
                    headers={'Content-Type': 'application/json',
                    'DD-API-KEY': '{}'.format(API_KEY),
                    'DD-APPLICATION-KEY': '{}'.format(APP_KEY)})
    print('Ddemoting old Dashboard for Condition Time')
except  Exception as e:
    print('Dashboard does not exist so cannot Ddemote')

print('Create Dashboard for Condition Time')
title1 = 'DEMO Condition Time'
widgets1 = [{'definition': {'type': 'timeseries',
            'requests': cond_ll(), 'title': 'Condition Apply Time'}}]


api.Dashboard.create(
    title=title1,
    widgets=widgets1,
    layout_type=layout_type1,
    description=description1,
    is_read_only=is_read_only1,
    notify_list=notify_list1,
    )


