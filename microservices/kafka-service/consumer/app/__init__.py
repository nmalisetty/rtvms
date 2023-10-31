import logging
from json import loads, dumps
import requests

from app.enum import EnvironmentVariables as EnvVariables
from kafka import KafkaConsumer


def invoke_alerting_service(message):
    server_ip = EnvVariables.ALERTING_SERVICE_SERVER.get_env()
    server_port = EnvVariables.ALERTING_SERVICE_PORT.get_env()
    endpoint = EnvVariables.ALERTING_SERVICE_ENDPOINT.get_env()

    print(type(server_ip))
    url = "http://{}:{}/{}".format(str(server_ip), int(server_port), str(endpoint))
    print(url)
    headers = {"Content-Type": "application/json"}
    message = dumps(message, indent=4)

    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print("Request successful")
        print("Response content:", response.content)
    else:
        print("Request failed with status code", response.status_code)


def alerts_consumer():
    try:
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_ALERT_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        print("alerts consumer connected")
        for message in consumer:
            print("message:", message)
            print("message type: ", type(message.value), "message value : ", message.value)
            if "Service_Type" in message.value and message.value["Service_Type"] == "Alert":
                invoke_alerting_service(message.value)

            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key, message.value))

    except Exception as e:
        print("in exception: ", str(e))
        logging.info('Connection successful', e)

