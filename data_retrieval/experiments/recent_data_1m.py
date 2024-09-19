import time
import json
from data_retrievers import DynamoDBRetriever, KinesisRetriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta

'''
Experiment description:


measure:

- time of the request in ms
- first returned item in s
- time when raw data returned from AWS in ms
- time after data processing to desired structure in ms
- number of requests needed to obtain the data


NOTE: WE DO NOT MEASURE HOW MANY REQUESTS PER MINUTE THE OPTION CAN HANDLE!
'''

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def run_experiment():
    devices_number = 100
    device_prefix = "test_"
    devices = [f"{device_prefix}{i}" for i in range(devices_number)]

    retrievers = [
        KinesisRetriever(),
        DynamoDBRetriever(),
        TimestreamDBRetriever()
    ]

    for device in devices:
        for retriever in retrievers:
            utc_date_time_start = datetime.now(timezone.utc)
            time_from = (utc_date_time_start - timedelta(minutes=1)).strftime(DATE_TIME_FORMAT)
            time_to = utc_date_time_start.strftime(DATE_TIME_FORMAT)
            response = retriever.retrieve(device, time_from, time_to, None, False)
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
            time.sleep(0.1)

            stats = {
                "device": device,
                "retriever": retriever.__class__.__name__,
                "start_time": time_to,
                "time_from": time_from,
                "latest_item_time": latest_item_time,
                "latest_item_delta": latest_item_delta,
                "records_length": records_length,
                "response_stats": response["stats"]
            }
            f = open(f"local/{retriever.__class__.__name__}_1m.txt", "a")
            f.write(f"{json.dumps(stats)}\n")
            f.close()
            # _format_print_stats(stats)
        time.sleep(1)


def _format_print_stats(stats: dict):
    print("---------------- stats ----------------")
    for key in stats.keys():
        print(f"{key:<15}: {stats[key]}")
