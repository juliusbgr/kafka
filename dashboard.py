import streamlit as st
from datetime import datetime
from collections import deque
from quixstreams import Application

# Buffers for temperature chart
temperature_buffer = deque(maxlen=100)
timestamp_buffer = deque(maxlen=100)

st.title("Real-Time IoT Dashboard")

@st.cache_resource
def get_kafka_app():
    return Application(
        broker_address="localhost:9092",
        consumer_group="dashboard",
        auto_offset_reset="latest",
    )

app = get_kafka_app()

sensor_topic = app.topic("sensor", value_deserializer="json")
alert_count_topic = app.topic("alert-count", value_deserializer="json")
avg_temp_topic = app.topic("avg-temp", value_deserializer="json")

col1, col2, col3 = st.columns(3)
temp_metric = col1.empty()
alert_count_metric = col2.empty()
avg_temp_metric = col3.empty()
temp_chart = st.empty()

previous_temp = None

with app.get_consumer() as consumer:
    consumer.subscribe([sensor_topic.name, alert_count_topic.name, avg_temp_topic.name])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        topic = msg.topic()

        if topic == sensor_topic.name:
            sensor_data = sensor_topic.deserialize(msg)
            temperature = sensor_data.value.get("temperature")
            device_id = sensor_data.value.get("device_id", "Unknown")
            timestamp_str = sensor_data.value.get("timestamp")
            timestamp = datetime.fromisoformat(timestamp_str)

            if previous_temp is None:
                delta = 0.0
            else:
                delta = temperature - previous_temp
            previous_temp = temperature

            temp_metric.metric(label=f"Device: {device_id}", value=f"{temperature:.2f} °C", delta=f"{delta:.2f} °C")

            timestamp_buffer.append(timestamp.strftime("%H:%M:%S"))
            temperature_buffer.append(temperature)

            temp_chart.line_chart(
                data={
                    "Time": list(timestamp_buffer),
                    "Temperature °C": list(temperature_buffer)
                },
                x="Time",
                y="Temperature °C",
                use_container_width=True,
            )

        elif topic == alert_count_topic.name:
            alert_data = alert_count_topic.deserialize(msg)
            alert_count = alert_data.value.get("alert_count", 0)
            alert_count_metric.metric(label="Alert Count (Last 5s)", value=alert_count)

        elif topic == avg_temp_topic.name:
            avg_temp_data = avg_temp_topic.deserialize(msg)
            avg_temp = avg_temp_data.value.get("avg_temp", 0.0)
            avg_temp_metric.metric(label="Avg Temp (Last 10s)", value=f"{avg_temp:.2f} °C")
