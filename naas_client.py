#!/usr/bin/env python3

import requests
import simplejson as json


class NaasClient:

    def __init__(self, url, token=None, **kwargs):
        self.url = url
        self.token = token
        self.api_username = kwargs.get("api_username", None)
        self.api_password = kwargs.get("api_password", None)
        self.net_username = kwargs.get("net_username", None)
        self.net_password = kwargs.get("net_password", None)
        self.device_type = kwargs.get("device_type", None)
        self.execution_type = kwargs.get("execution_type", "execution")
        self.host = kwargs.get("host", None)
        self.commands = kwargs.get("commands", None)

        if not isinstance(self.commands, list):
            self.commands = (self.commands,)

    def create_token(self):
        if self.api_username and self.api_password:
            data = {"username": self.api_username, "password": self.api_password}
            endpoint = f"{self.url}auth/"
            result = requests.post(endpoint, data=data)

            return json.loads(result.content)

        return json.loads({"Error": "API Username or Password not known."})

    def get(self, id=None):
        if id:
            endpoint = f"{self.url}netmiko/{id}/"
        else:
            endpoint = f"{self.url}netmiko/"

        headers = {
            "Authorization": f"Token {self.token}"
        }

        if self.token:
            result = requests.get(endpoint, headers=headers)

            return json.loads(result.content)

        return json.loads({"Error": "Auth Token not loaded."})

    def post(self):
        required = [self.net_username, self.net_password, self.token, self.host, self.device_type, self.commands]
        if all(required):
            headers = {
                "Authorization": f"Token {self.token}",
                "NETAUTH": f"{self.net_username}:{self.net_password}"
            }
            data = {
                "host": self.host,
                "device_type": self.device_type,
                "execution_type": self.execution_type,
                "commands": self.commands
            }
            endpoint = f"{self.url}netmiko/"
            result = requests.post(endpoint, data=data, headers=headers)

            return json.loads(result.content)

        return json.loads({"Error": "Required options missing.",
                           "Required": ["net_username", "net_password", "token", "host", "device_type", "commands"]})
