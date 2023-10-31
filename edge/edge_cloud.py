import json
import threading
import pandas as pd
from datetime import datetime
from json import loads
from queue import Queue
import requests
from kafka import KafkaConsumer
import streamlit as st
import time
from interface.src.generator import generate_data, GetDataFrame
from interface.utils.get_conditions import MyConditionsData

# Set up the app layout
st.set_page_config(page_title='Real-time Vehicle Monitoring System (Edge to Cloud)', layout='wide')
st.title('Real-time Vehicle Monitoring System (Edge to Cloud)')

# Reading conditions from json file
conditions = MyConditionsData("interface/conditions/Beacon_conditions.json")


def create_container():
    return st.container()


def create_charts(chart_columns):
    num_columns = 4
    columns = st.columns(num_columns)
    charts = {}
    for i, column in enumerate(chart_columns):
        if column != 'timestamp':
            chart = columns[i % num_columns].line_chart(
                get_initial_sample_data(chart_columns, df.loc[0]).set_index('timestamp').loc[:, column])
            charts[column] = chart
    return charts


@st.cache_resource
def getiter_dataframe():
    get_dataframe = GetDataFrame(conditions.get("file_path"), conditions)
    df, chat_columns = get_dataframe.dataframe()
    # Get an iterator over the rows of the DataFrame
    df_iter = iter(df.itertuples(index=False))
    return df, chat_columns, df_iter


def get_initial_sample_data(chart_columns, row):
    sample_df = pd.DataFrame(columns=chart_columns)
    sample_df.loc[0] = row
    sample_df['timestamp'] = [pd.Timestamp.now()]
    sample_df['timestamp'] = pd.to_datetime(sample_df['timestamp'])
    return sample_df


def send_data_cloud(data, id, crash, url):
    payload = {"source": "edge",
               "type": "streaming",
               "id": id,
               "timeStamp": datetime.now(),
               "data": data,
               "crash": crash
               }
    headers = {"Content-Type": "application/json"}
    message = json.dumps(payload, indent=4, default=str)
    response = requests.post(url, data=message, headers=headers)
    if response.status_code == requests.codes.ok:
        print('Data sent to cloud')
        if crash:
            return False
    return True


def add_data_carts(data_dict, charts, c):
    try:
        data_df = pd.DataFrame.from_dict(data_dict)
        data_df = data_df.rename(columns=conditions.get("display_columns"))
        for column in chart_columns:
            if column != 'timestamp':
                charts[column].add_rows(data_df[['timestamp', column]].set_index('timestamp').loc[:, column])
        with chart_container:
            st.experimental_set_query_params(chart_update=c)

    except Exception as e:
        print(e)


def beacon_consumer(messages_queue):
    kafka_consumer = KafkaConsumer(
        "beacons",
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    for message in kafka_consumer:
        if conditions.get("id") != message.value["id"]:
            messages_queue.put("Vehicle {} crashed at the location lat : {}  long:{}".format(message.value["id"], str(
                message.value['data']['location']['lat']), str(message.value['data']['location']['lat'])))


def ack_consumer(messages_queue):
    kafka_consumer = KafkaConsumer(
        "alerts",
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    for message in kafka_consumer:
        if conditions.get("id") == message.value["id"]:
            messages_queue.put("Real-time alert: " + message.value["data"]["type"])


def run(charts, df_iter, message_queue):
    c = 0
    chart_count = 0
    data = []
    notifications = []
    prev_length = len(notifications)
    start_time = time.time()
    crash = conditions.get("Crash")
    speed = 0
    while True:
        while not messages_queue.empty():
            message = messages_queue.get()
            print(message)
            if "lat" in message:
                notifications.append({"type": "info", "message": message})
                crash = False
            else:
                notifications.append({"type": "error", "message": message})

        data_dict, data_dict1 = generate_data(df_iter, start_time, conditions, speed)
        if c >= 100:
            c = 0
            if not send_data_cloud(data, conditions.get("id"), crash, "http://127.0.0.1:8003/edge/streaming_data"):
                crash = False
            data.clear()
        data_dict1 = {conditions.get("entire_columns").get(key, key): value for key, value in data_dict1.items()}
        data.append(data_dict1)
        if conditions.get("Speeding"):
            speed += 1
        if data_dict is None:
            break
        add_data_carts(data_dict, charts, chart_count)
        chart_count += 1
        time.sleep(0.1)
        c += 1
        if notifications and len(notifications) > prev_length:
            prev_length = len(notifications)
            with notification_container:
                with notification_container:
                    notif = notifications[-1]
                    if notif["type"] == "error":
                        notif_message = f"{notif['message']}"
                        st.warning(notif_message, icon="⚠️")
                    else:
                        notif_message = f"{notif['message']}"
                        st.info(notif_message, icon="ℹ️")
            notification_container.empty()


notification_container = create_container()
with notification_container:
    st.write("Notifications :")
chart_container = create_container()
messages_queue = Queue()
kafka_consumer_beacon = threading.Thread(target=beacon_consumer, args=(messages_queue,))
kafka_consumer_beacon.start()
kafka_consumer_alert = threading.Thread(target=ack_consumer, args=(messages_queue,))
kafka_consumer_alert.start()
df, chart_columns, df_iter = getiter_dataframe()
charts = create_charts(chart_columns)
run(charts, df_iter, messages_queue)
