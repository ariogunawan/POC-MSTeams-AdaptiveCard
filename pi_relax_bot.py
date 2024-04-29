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
    real_endpoint_url = ('https://prod-14.australiasoutheast.logic.azure.com:443/workflows'
                         '/beac23393d494ec99573e7221c69b422'
                         '/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig'
                         '=ypPqNZk4kUPN5dMLChnhc9sG9dd4YCUsyknzMKBLnxg')  #real
    endpoint_url = ('https://prod-15.australiasoutheast.logic.azure.com:443/workflows'
                    '/edb9b3f5aa2a4378b9a7c0558a9b5773/triggers/manual/paths/invoke?api-version=2016-06-01&sp'
                    '=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Pzx9j1cLkFPmKIbIkepYvuQPN1cEU4NeNrQGnUsQILI')  #testing

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
json_data = open(r'C:\Users\axg067_dev\PycharmProjects\quotesOfTheDay\relaxbot_adaptivecard.json', 'r',
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
