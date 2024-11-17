import time
import json
from data_retrievers import DynamoDBRetriever, KinesisRetriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta

DYNAMODB_TABLE = "aq_measurements_experiment"
S3_BUCKET = "idealaq-aq-measurements-bucket"
KINESIS_STREAM_NAME = "aq-data-stream"
TIMESTREAM_DATABASE = "aq-time-stream"
TIMESTREAM_TABLE = "aq_data"

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


DEVICES = 100
def run_experiment():
    device_prefix = "test_"
    leading_zeros = 2
    devices = [f"{device_prefix}{i:0{leading_zeros}}" for i in range(DEVICES)]

    # attributes = ["key05"]
    attributes = None

    retrievers = [
        KinesisRetriever(KINESIS_STREAM_NAME),
        DynamoDBRetriever(DYNAMODB_TABLE),
        TimestreamDBRetriever(TIMESTREAM_DATABASE, TIMESTREAM_TABLE)
    ]

    for device in devices:
        print(f"Device: {device}")
        for retriever in retrievers:
            print(f" - Retriever: {retriever.__class__.__name__}")
            utc_date_time_start = datetime.now(timezone.utc)
            time_from = (utc_date_time_start - timedelta(seconds=1799)).strftime(DATE_TIME_FORMAT)
            time_to = utc_date_time_start.strftime(DATE_TIME_FORMAT)
            response = retriever.retrieve(device, time_from, time_to, attributes, False)
            records = response["records"]
            records_length = len(records)
            latest_item_time = None
            latest_item_delta = None
            if records_length > 0:
                latest_item = records[-1]
                latest_item_time = latest_item["time"]
                dt1 = datetime.strptime(time_to, DATE_TIME_FORMAT)
                dt2 = datetime.strptime(latest_item_time, DATE_TIME_FORMAT)
                latest_item_delta = (dt2 - dt1).total_seconds()

                f = open(f"../local/recent_30m_all_attr/devices/{retriever.__class__.__name__}_{device}_30m.txt", "a")
                for record in records:
                    f.write(f"{json.dumps(record)}\n")
                f.close()

            time.sleep(0.1)

            stats = {
                "device": device,
                "retriever": retriever.__class__.__name__,
                "start_time": time_to,
                "time_from": time_from,
                "time_to": time_to,
                "latest_item_time": latest_item_time,
                "latest_item_delta": latest_item_delta,
                "records_length": records_length,
                "response_stats": response["stats"]
            }
            f = open(f"../local/recent_30m_all_attr/{retriever.__class__.__name__}_30m.txt", "a")
            f.write(f"{json.dumps(stats)}\n")
            f.close()
