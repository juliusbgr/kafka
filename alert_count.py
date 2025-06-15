import logging
from quixstreams import Application
from quixstreams.dataframe.windows import Count
from datetime import timedelta

def run_alert_count_pipeline():
    logging.info("Starting alert count pipeline...")

    app = Application(
        broker_address="localhost:9092",
        consumer_group="alert-counter",
        auto_offset_reset="latest",
    )

    alert_topic = app.topic("alert", value_deserializer="json")
    alert_count_topic = app.topic("alert-count", value_serializer="json")

    df = app.dataframe(alert_topic)
    df = (
        df.hopping_window(duration_ms=timedelta(seconds=5), step_ms=timedelta(seconds=1))
          .agg(alert_count=Count())
          .final()
    )

    df.to_topic(alert_count_topic)

    app.run(df)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_alert_count_pipeline()
