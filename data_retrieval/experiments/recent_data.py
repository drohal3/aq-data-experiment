import time
from data_retrievers import AbstractRetriever, DynamoDBRetriever, KinesisRetriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta
import asyncio

'''
Experiment description:

loop through every device, each device concurrently runs every design option

measure:

- time of the request in ms
- first returned item in s
- time when raw data returned from AWS in ms
- time after data processing to desired structure in ms
- number of requests needed to obtain the data


NOTE: WE DO NOT MEASURE HOW MANY REQUESTS PER MINUTE THE OPTION CAN HANDLE!
'''

def run_experiment():
    # TODO: redo
    devices_number = 1
    device_prefix = "test_"
    devices = [f"{device_prefix}{i}" for i in range(devices_number)]

    print(devices)

    retrievers = [
        # DynamoDBRetriever(),
        KinesisRetriever(),
        # TimestreamDBRetriever()
    ]

    get_recent_data(devices, retrievers)

def get_recent_data(devices: list[str], retrievers: list[AbstractRetriever]) -> None:
    loop = asyncio.get_event_loop()
    tasks = []
    for retriever in retrievers:
        tasks.append(_run_task(retriever, devices))

    loop.run_until_complete(asyncio.gather(*tasks))

async def _run_task(retriever: AbstractRetriever, devices: list[str]) -> None:
    stats = {
        "retriever": retriever.__class__.__name__
    }

    def retrieve(device_s: str, time_from_s: str, time_to_s: str):
        retriever.retrieve(device_s, time_from_s, time_to_s, None, False)

    loop = asyncio.get_running_loop()
    for device in devices:
        print(f"START {retriever.__class__.__name__} retrieving data for {device}")
        utc_date_time_start = datetime.now(timezone.utc)
        time_from = (utc_date_time_start - timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
        time_to = utc_date_time_start.strftime("%Y-%m-%d %H:%M:%S")
        response = await loop.run_in_executor(
            None,
            retrieve,
            device,
            time_from,
            time_to
        )
        print(f"END {retriever.__class__.__name__} retrieving data for {device}")
        await asyncio.sleep(1)

    print(stats)
