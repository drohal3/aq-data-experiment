import time
import json
from data_retrievers import S3Retriever, DynamoDBRetriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta

DYNAMODB_TABLE = "aq_measurements_experiment"
S3_BUCKET = "idealaq-aq-measurements-bucket"
KINESIS_STREAM_NAME = "aq-data-stream"
TIMESTREAM_DATABASE = "aq-time-stream"
TIMESTREAM_TABLE = "aq_data"

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

TIME_FROM = "2024-10-18 12:00:00"
TIME_TO = "2024-10-19 11:59:59"


DEVICES = 100
def run_experiment():
    device_prefix = "test_"
    leading_zeros = 2
    devices = [f"{device_prefix}{i:0{leading_zeros}}" for i in range(DEVICES)]

    attributes = ["key05"]
    # attributes = None

    retrievers = [
        DynamoDBRetriever(DYNAMODB_TABLE),
        S3Retriever(S3_BUCKET),
        TimestreamDBRetriever(TIMESTREAM_DATABASE, TIMESTREAM_TABLE)
    ]

    for device in devices:
        print(f"Device: {device}")
        for retriever in retrievers:
            print(f" - Retriever: {retriever.__class__.__name__}")
            utc_date_time_start = datetime.now(timezone.utc)
            time_from = TIME_FROM
            time_to = TIME_TO
            start_time = utc_date_time_start.strftime(DATE_TIME_FORMAT)
            response = retriever.retrieve(device, time_from, time_to, attributes, False)
            records = response["records"]
            records_length = len(records)
            latest_item_time = None
            first_item_time = None
            if records_length > 0:
                latest_item = records[-1]
                latest_item_time = latest_item["time"]

                first_item = records[0]
                first_item_time = first_item["time"]

                f = open(f"local/arch_1d_all_attr/devices/{retriever.__class__.__name__}_{device}.txt", "a")
                for record in records:
                    f.write(f"{json.dumps(record)}\n")
                f.close()

            utc_date_time_end = datetime.now(timezone.utc)
            end_time = utc_date_time_end.strftime(DATE_TIME_FORMAT)

            # time.sleep(0.1)

            stats = {
                "device": device,
                "retriever": retriever.__class__.__name__,
                "start_time": start_time,
                "end_time": end_time,
                "time_from": time_from,
                "time_to": time_to,
                "latest_item_time": latest_item_time,
                "first_item_time": first_item_time,
                "records_length": records_length,
                "response_stats": response["stats"]
            }
            f = open(f"local/arch_1d_all_attr/{retriever.__class__.__name__}.txt", "a")
            f.write(f"{json.dumps(stats)}\n")
            f.close()
