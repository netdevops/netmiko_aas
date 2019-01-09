#!/usr/bin/env python3

import requests
import time
import simplejson as json
from getpass import getpass


def get_credentials():
    print("Enter Network Device Credentials.")
    return f"{input('Username: ')}:{getpass('Password: ')}"


def get_token():
    print("Enter API Auth Token.")
    return f"Token {input('Token: ')}"


headers = {
    "Authorization": get_token(),
    "NETAUTH": get_credentials(),
}
url = "http://localhost:8000/api/v1/netmiko/"
data = {
    "host": "watch",
    "device_type": "linux",
    "commands": ["ping -c 2 1.1.1.1"]
}
post_request = requests.post(url, headers=headers, data=data)
max_loops = 100
start_loop = 1

if post_request.status_code == 201:
    result = json.loads(post_request.content)
    id = result["id"]
    while start_loop <= max_loops:
        get_request = requests.get(f"{url}{id}/", headers=headers)
        get_result = json.loads(get_request.content)
        if get_request.status_code == 200:
            if get_result["completed"]:
                print(get_result["output"])
                start_loop = 101
        else:
            print(f"ERROR: GET Code - {get_request.status_code}")
            break
        start_loop += 1
        time.sleep(1)
else:
    print(f"ERROR: POST Code - {post_request.status_code}")