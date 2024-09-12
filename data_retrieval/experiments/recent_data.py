import time

from data_retrieval.data_retrievers import AbstractRetriever
from datetime import datetime, timezone, timedelta
import asyncio
def get_recent_data(devices: list[str], retrievers: list[AbstractRetriever]) -> None:
    loop = asyncio.get_event_loop()
    tasks = []
    for retriever in retrievers:
        tasks.append(_run_task(retriever, devices))

    loop.run_until_complete(asyncio.gather(*tasks))

async def _run_task(retriever: AbstractRetriever, devices: list[str]) -> None:
    def retrieve():
        retriever.retrieve(device, time_from, time_to)

    loop = asyncio.get_running_loop()
    for device in devices:
        utc_date_time_start = datetime.now(timezone.utc)
        time_from = (utc_date_time_start - timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
        time_to = utc_date_time_start.strftime("%Y-%m-%d %H:%M:%S")
        response = await loop.run_in_executor(None, retrieve, device, time_from, time_to)
        await asyncio.sleep(1)
