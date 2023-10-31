import json
import requests


def send_beacon(url, data):
    headers = {"Content-Type": "application/json"}
    beacon = {
        "type": "beacon",
        "source": "edge",
        "id": data,
        "data": {
            "timestamp": "1681870109",
            "location": {
                "lat": 39.168408,
                "lng": -86.499282
            },
            "make": "Nissan"
        }
    }
    message = json.dumps(beacon, indent=4)
    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print('Beacon sent')
        send_beacon_mail(data, beacon)


def send_beacon_mail(source, beacon):
    message_1 = "The vehicle {} crashed at lat : {} long : {}  at time : {} ".format(str(source), str(beacon["data"]["location"]["lat"]), str(beacon["data"]["location"]["lng"]), str(beacon["data"]["timestamp"]))
    request_body = {'from_': 'example@example.com', 'to': 'example@example.com', 'subject': 'Alert raised by' + str(source), 'message': message_1 }
    server_ip = "localhost"
    server_port = "4000"
    endpoint = "alert/email"

    print(type(server_ip))
    url = "http://{}:{}/{}".format(str(server_ip), int(server_port), str(endpoint))
    print(url)
    headers = {"Content-Type": "application/json"}
    message = json.dumps(request_body, indent=4)

    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print("Request successful")
        print("Response content:", response.content)
    else:
        print("Request failed with status code", response.status_code)