# Real-Time IoT Sensor Stream Processing

A complete real-time streaming solution for simulated IoT temperature sensors using **Apache Kafka**, **Quix Streams**, and **Streamlit**. 

This project demonstrates data ingestion, filtering, windowed aggregations, and a live dashboard to monitor alerts and temperature KPIs.

---

## 📖 Overview

The system processes simulated temperature sensor data in real time, performing:

- High-temperature alert filtering
- Counting alerts in a sliding 5-second window
- Calculating average temperature over a sliding 10-second window
- Displaying live metrics and charts in a Streamlit dashboard

This extends the base exercise described in `kafka_Roland.md` by adding advanced windowed aggregations and a responsive UI.

---

## 🏗 Architecture

| Component                      | Description                                                         | Kafka Topic(s)         |
| ----------------------------- | ------------------------------------------------------------------ | ---------------------- |
| **Producer** (`producer.py`)  | Simulates sensor temperature readings every second                 | `sensor`               |
| **Alert Filter** (`consumer.py`) | Filters high temperature data (Kelvin > 303)                      | `alert`                |
| **Alert Counter** (`alert_counter.py`) | Aggregates alert counts over 5-second hopping window             | `alert-count`          |
| **Average Temperature Tracker** (`avg_temp.py`) | Computes average temperature over 10-second hopping window       | `avg-temp`             |
| **Dashboard** (`dashboard.py`) | Streamlit app visualizing device temps, alert counts, averages, and charts | Consumes all above     |

---

## 🚀 Getting Started

### 1. Launch Kafka Broker

Run Kafka using Docker Compose:

```bash
docker compose up -d
