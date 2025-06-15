IoT Sensor Data Streaming & Analytics

This project showcases a real-time data processing system for simulated IoT temperature sensors, leveraging Apache Kafka, Quix Streams, and a Streamlit dashboard for instant insights.

Building on the baseline exercise described in kafka_Roland.md, it adds sophisticated capabilities such as:

    Aggregating alert events over sliding time windows

    Calculating rolling average temperatures

    Visualizing metrics dynamically in an interactive UI

Architecture Overview

The solution is structured around five key components:

    Data Producer (producer.py)
    Simulates a sensor generating temperature readings every second, publishing raw data to the Kafka sensor topic.

    Alert Filtering Consumer (consumer.py)
    Listens to the sensor stream, identifies high-temperature readings (above 303 Kelvin), and pushes these alerts into an alert topic.

    Alert Count Aggregator (alert_counter.py)
    Reads from the alert topic, counts alerts within a rolling 5-second window, and publishes the counts to alert-count.

    Average Temperature Calculator (avg_temp.py)
    Computes the average temperature from sensor data over a 10-second hopping window, outputting results to avg-temp.

    Dashboard Application (dashboard.py)
    Streamlit-powered frontend showing live device temperatures, alert counts, average temperature trends, and a historical temperature graph.

Getting Started
Step 1: Launch Kafka

Start your Kafka environment using Docker Compose:

docker compose up -d

Step 2: Run Processing Pipelines

Open separate terminals and launch each of the following:

python consumer.py        # Processes raw data into alerts
python alert_counter.py   # Calculates alert counts over 5-second windows
python avg_temp.py        # Computes average temperature over 10-second windows

Step 3: Start the Dashboard

Launch the real-time monitoring UI:

streamlit run dashboard.py

Kafka Topic Breakdown
Topic Name	Purpose
sensor	Original simulated sensor temperature readings
alert	High-temperature events extracted from sensor data
alert-count	Number of alerts aggregated over recent 5 seconds
avg-temp	Rolling average temperature calculated over 10 seconds
Installation & Dependencies

Use uv for managing Python dependencies:

uv init
uv add streamlit quixstreams

Alternatively, install packages via the provided requirements.txt.
Key Concepts & Features

    Quix Streaming DataFrames enable declarative, easy-to-read streaming transformations.

    Time-based Hopping Windows provide flexible, overlapping intervals for smooth KPI calculations.

    Streamlit Layouts use columns to arrange multiple live metrics side by side for a clean dashboard view.

Visuals

Explore the included screenshots to see the dashboard’s real-time visualization in action.
