#!/usr/bin/python3.6
import requests
import json
import sys

if __name__ == '__main__':

    wekbook_url = 'https://hooks.slack.com/services/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'
    val = sys.argv[1:]
    #print(value)
    data = {
        'text': str(val)
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))

