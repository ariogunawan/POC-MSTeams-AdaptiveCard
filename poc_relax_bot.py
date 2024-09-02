import json

import httpx
from httpx import Response
import time


class BoredAPI:
    personal_access_token = None
    header = None
    endpoint_url = 'http://www.boredapi.com/api/'

    def __init__(self):
        pass

    def send_request(self, method: str, resource: str = None, payload: str = None) -> Response:
        if method.lower() == 'get':
            payload = None
        resource_url = self.endpoint_url + resource
        return httpx.request(method=method, url=resource_url, headers=self.header, content=payload, verify=False)

    def request_activity(self) -> Response:
        method = 'get'
        path = 'activity'
        resource = path + '/'
        payload = None
        return self.send_request(method=method, resource=resource, payload=payload)


class TeamsWebhookAPI:
    personal_access_token = None
    header = {'Content-Type': 'application/json'}
    real_endpoint_url = ('')  #real
    endpoint_url = ('')  #testing

    def __init__(self):
        pass

    def send_request(self, method: str, resource: str = None, payload: str = None) -> Response:
        if method.lower() == 'get':
            payload = None
        resource_url = self.endpoint_url + resource
        return httpx.request(method=method, url=resource_url, headers=self.header,
                             content=json.dumps(payload).encode('utf-8'),
                             verify=False)

    def post_message(self, payload) -> Response:
        method = 'post'
        path = ''
        resource = path
        return self.send_request(method=method, resource=resource, payload=payload)


# Initiate object
bored = BoredAPI()
response: Response = bored.request_activity()
activity = response.json()['activity']
activity = activity[0].lower() + activity[1:]
quotes = f"{activity}"
print(quotes)

# Get JSON data
json_data = open(r'relaxbot_adaptivecard.json', 'r',
                 encoding='utf-8')
data = json.load(json_data)
data["attachments"][0]["content"]["body"][0]["columns"][0]["items"][0]["columns"][0]["items"][0][
    "text"] = "\uD83E\uDD16 **P&I Relax Bot v0.1**"
data["attachments"][0]["content"]["body"][1]["text"] = f"Stop testing, _{quotes}_ instead \uD83D\uDCE3"
print(data)
teams = TeamsWebhookAPI()
response: Response = teams.post_message(payload=data)
print(response)
time.sleep(5)  # Sleep for 3 seconds
