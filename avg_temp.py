import logging
from quixstreams import Application
from quixstreams.dataframe.windows import Mean
from datetime import timedelta

def run_avg_temp_pipeline():
    logging.info("Starting average temperature pipeline...")

    app = Application(
        broker_address="localhost:9092",
        consumer_group="avg-temp",
        auto_offset_reset="latest",
    )

    sensor_topic = app.topic("sensor", value_deserializer="json")
    avg_temp_topic = app.topic("avg-temp", value_serializer="json")

    df = app.dataframe(sensor_topic)
    df = (
        df.hopping_window(duration_ms=timedelta(seconds=10), step_ms=timedelta(seconds=1))
          .agg(avg_temp=Mean("temperature"))
          .final()
    )

    df.to_topic(avg_temp_topic)

    app.run(df)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_avg_temp_pipeline()
