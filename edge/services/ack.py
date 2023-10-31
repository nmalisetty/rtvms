import json
import requests

ack = {
    "type": "ack",
    "source": "edge",
    "id": "edge-002",
    "data": {
        "timestamp": "1681870109",
        "location": {
            "lat": 39.168408,
            "lng": -86.499282
        },
        "make": "Nissan",
        "responding": True,
        "destination": {
            "id": "edge-001",
            "location": {
                "lat": 39.168408,
                "lng": -86.499282
            }
        }
    }
}


def send_ack(url):
    headers = {"Content-Type": "application/json"}
    message = json.dumps(ack, indent=4)
    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print('Acknowledgement sent')
