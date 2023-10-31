import ack


def beacon_consumer(kafka_consumer):
    records = kafka_consumer.poll(1000, 500)
    if records:
        for message in records:
            if 'type' in message.value and message.value['type'] == 'beacon':
                print('Beacon received')
                print(message.value)
                ack.send_ack('http://localhost:8000/producer/acks')


def ack_consumer(kafka_consumer):
    records = kafka_consumer.poll(1000, 500)
    if records:
        for message in records:
            if 'type' in message.value and message.value['type'] == 'ack':
                print('Acknowledgement received')
                print(message.value)



