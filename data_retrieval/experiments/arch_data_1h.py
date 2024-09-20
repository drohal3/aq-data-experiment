import time
import json
from data_retrievers import DynamoDBRetriever, S3Retriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DEVICES = 1

# TODO: adjust
DATA_FROM = "2024-09-19 08:00:00"
DATA_TO = "2024-09-19 17:59:59"

def run_experiment():
    device_prefix = "test_"
    devices = [f"{device_prefix}{i}" for i in range(DEVICES)]

    retrievers = [
        S3Retriever(),
        DynamoDBRetriever(),
        TimestreamDBRetriever()
    ]

    for device in devices:
        for retriever in retrievers:
            utc_date_time_start = datetime.now(timezone.utc)
            time_from = DATA_FROM
            time_to = DATA_TO
            start_time = utc_date_time_start.strftime(DATE_TIME_FORMAT)
            stats_loops = []
            records_r = []
            while True:
                response = retriever.retrieve(device, time_from, time_to, None, False)
                records = response["records"]
                records_r.extend(records)
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
                    if latest_item_delta > 2:
                        time_from = (dt2 + timedelta(seconds=1)).strftime(DATE_TIME_FORMAT)
                        time.sleep(1)
                        continue
                time.sleep(0.1)
                break

            stats = {
                "device": device,
                "retriever": retriever.__class__.__name__,
                "start_time": start_time,
                "requests": stats_loops
            }
            f = open(f"local/arch_1h/{retriever.__class__.__name__}_arch1h.txt", "a")
            f.write(f"{json.dumps(stats)}\n")
            f.close()

            f = open(f"local/arch_1h/devices/{device}_{retriever.__class__.__name__}_data.txt", "a")
            for d in records_r:
                f.write(f"{json.dumps(d)}\n")
            f.close()
