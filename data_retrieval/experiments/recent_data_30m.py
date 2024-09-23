import time
import json
from data_retrievers import DynamoDBRetrieverV2, KinesisRetriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

MINUTES = 30
DEVICES = 100

def run_experiment():
    device_prefix = "test_"
    devices = [f"{device_prefix}{i}" for i in range(DEVICES)]

    retrievers = [
        KinesisRetriever(),
        DynamoDBRetrieverV2(),
        TimestreamDBRetriever()
    ]

    for device in devices:
        for retriever in retrievers:
            print(f"requesting... device: {device}, retriever: {retriever.__class__.__name__}")
            utc_date_time_start = datetime.now(timezone.utc)
            time_from = (utc_date_time_start - timedelta(minutes=MINUTES)).strftime(DATE_TIME_FORMAT)
            time_to = utc_date_time_start.strftime(DATE_TIME_FORMAT)
            stats_loops = []
            response = retriever.retrieve(device, time_from, time_to, None, False)
            records = response["records"]
            records_length = len(records)

            if records_length > 0:
                latest_item = records[-1]
                latest_item_time = latest_item["time"]
                dt1 = datetime.strptime(time_to, DATE_TIME_FORMAT)
                dt2 = datetime.strptime(latest_item_time, DATE_TIME_FORMAT)
                latest_item_delta = (dt2 - dt1).total_seconds()
                stats_loops.append({
                    "time_from": time_from,
                    "time_to": time_to,
                    "records_length": records_length,
                    "latest_item_time": latest_item_time,
                    "latest_item_delta": latest_item_delta,
                    "response_stats": response["stats"]
                })

                f = open(f"local/recent_30m/devices/{retriever.__class__.__name__}_{device}_30m.txt", "a")
                for record in records:
                    f.write(f"{json.dumps(record)}\n")
                f.close()

                time.sleep(0.01)

            stats = {
                "device": device,
                "retriever": retriever.__class__.__name__,
                "start_time": time_to,
                "requests": stats_loops
            }
            _format_print_stats(stats)
            f = open(f"local/recent_30m/{retriever.__class__.__name__}_30m.txt", "a")
            f.write(f"{json.dumps(stats)}\n")
            f.close()
            _format_print_stats(stats)


def _format_print_stats(stats: dict):
    print("---------------- stats ----------------")
    for key in stats.keys():
        print(f"{key:<15}: {stats[key]}")
