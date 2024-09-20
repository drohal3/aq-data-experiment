from botocore.exceptions import ClientError

from .abstract_retriever import AbstractRetriever
import boto3
import time
from datetime import datetime, timedelta

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class DynamoDBRetrieverV2(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def _retrieve_raw(
            self, device: str, data_from: str, data_to: str, attributes: list | None = None
    ) -> dict:
        if attributes is not None:
            raise NotImplementedError
        # TODO: consequent requests if data cut
        start_time = time.time()

        request_from = data_from
        request_to = data_to

        items = []
        err_count = 0
        err_count_total = 0
        requests_count = 0
        req_stats = []
        while True:
            if err_count > 3:
                break
            try:
                requests_count += 1
                req_start_time = time.time()
                response = self.client.query(
                    TableName="aq_measurements_experiment",
                    Select="ALL_ATTRIBUTES",
                    KeyConditionExpression='device_id = :device_id AND #time BETWEEN :data_from AND :data_to',
                    ExpressionAttributeNames={
                        '#time': 'time'
                    },
                    ExpressionAttributeValues={
                        ':device_id': {'S': device},
                        ':data_from': {'S': request_from},
                        ':data_to': {'S': request_to}
                    }
                )
                req_end_time = time.time()

                items_curr = response['Items']

                items_curr_length = len(items_curr)

                stats = {
                    "start_time": req_start_time,
                    "end_time": req_end_time,
                    "elapsed": req_end_time - req_start_time,
                    "items": items_curr_length,
                    "data_from": request_from,
                    "data_to": request_to,
                    "first_item": None,
                    "last_item": None
                }

                if items_curr_length > 0:
                    err_count = 0

                    items.extend(items_curr)
                    first_item = items_curr[0]
                    first_item_time = first_item['time']["S"]
                    last_item = items_curr[-1]
                    last_item_time = last_item['time']["S"]

                    date = datetime.strptime(last_item_time, DATE_TIME_FORMAT)
                    request_from = (date + timedelta(seconds=1)).strftime(DATE_TIME_FORMAT)

                    stats["last_item"] = last_item_time
                    stats["first_item"] = first_item_time

                    if last_item_time < data_to:
                        req_stats.append(stats)
                        continue
                req_stats.append(stats)
            except Exception:
                err_count += 1
                err_count_total += 1
                time.sleep(err_count)
                continue
            break

        end_time = time.time()

        return {
            "records": {
                "items": items
            },
            "stats": {
                "start_time": start_time,
                "end_time": end_time,
                "elapsed": end_time - start_time,
                "err_request_count": err_count_total,
                "requests_count": requests_count,
                "req_stats": req_stats
            }
        }

    def _format(self, raw_data: dict) -> list:
        items = raw_data["items"]
        processed = []

        for item in items:
            # device_id = item["device_id"]["S"]
            sample_data = item["sample_data"]["M"]
            parameters = {}

            for key in sample_data.keys():
                sample_data_data = sample_data[key]
                parameters[key] = sample_data_data[next(iter(sample_data_data))]
            processed.append(parameters)

        return processed
