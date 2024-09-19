import time
import json
from data_retrievers import DynamoDBRetriever, S3Retriever, TimestreamDBRetriever
from datetime import datetime, timezone, timedelta

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

MINUTES = 30
DEVICES = 100

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
            pass
