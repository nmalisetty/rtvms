from datetime import datetime

import requests
import json

from json import loads, dumps
from datetime import datetime

def send_alert(alert_message,subject):
    # send alert mail
    request_body = {'from_': 'example@example.com', 'to': 'example@example.com', 'subject':subject, 'message': alert_message }
    server_ip = "localhost"
    server_port = "4000"
    endpoint = "alert/email"

    print(type(server_ip))
    url = "http://{}:{}/{}".format(str(server_ip), int(server_port), str(endpoint))
    print(url)
    headers = {"Content-Type": "application/json"}
    message = dumps(request_body, indent=4)

    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print("Request successful")
        print("Response content:", response.content)
    else:
        print("Request failed with status code", response.status_code)

def send_alert_kafka(message,id,url):
    alert = {
        "type": "alert",
        "source": "edge",
        "id": id,
        "data": {
            "type": message,
            "priority": "high",
            "alert": True
        }
    }

    headers = {"Content-Type": "application/json"}
    payload = json.dumps(alert, indent=4)
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == requests.codes.ok:
        print('Alert sent')
    message_1 = "Realtime time alert from {} : {} having priority {} ".format(id, str(message),str(alert["data"]["priority"]))
    send_alert(message_1,message)

def send_beacon_kafka(data,id,url):
    beacon = {
        "type": "beacon",
        "source": "edge",
        "id": id,
        "data": {
            "timestamp": " 16863253453",
            "location": {
                "lat": 39.168408,
                "lng": -86.499282
            },
            "make": "Nissan"
        }
    }

    headers = {"Content-Type": "application/json"}
    message = json.dumps(beacon, indent=4)
    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print('Beacon sent')
    message = "The vehicle {} crashed at lat : {} long : {}  at time : {} ".format(id,str(beacon["data"]["location"]["lat"]),str(beacon["data"]["location"]["lng"]),str(beacon["data"]["timestamp"]))
    send_alert(message,"Crash Alert")