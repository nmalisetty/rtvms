import json
import requests


def send_alert(url, data, alert_type):
    headers = {"Content-Type": "application/json"}
    alert = {
        "type": "alert",
        "source": "edge",
        "id": data,
        "data": {
            "type": alert_type,
            "priority": "high",
            "alert": True
        }
    }
    message = json.dumps(alert, indent=4)
    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print('Alert sent')


def send_alert_mail(source, message):
    message_1 = "Realtime time alert From {} : {}, having priority high ".format(str(source), str(message))
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
