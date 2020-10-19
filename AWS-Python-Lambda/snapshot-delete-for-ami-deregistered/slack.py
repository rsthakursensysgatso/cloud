import requests
import json
import sys

if __name__ == '__main__':

    wekbook_url = 'https://hooks.slack.com/services/xsfdsf'
    val = sys.argv[1:]
    #print(value)
    data = {
        'text': str(val)
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))


