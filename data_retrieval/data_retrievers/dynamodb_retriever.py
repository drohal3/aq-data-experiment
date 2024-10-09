from .abstract_retriever import AbstractRetriever
import boto3
import time
from datetime import datetime, timedelta

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class DynamoDBRetriever(AbstractRetriever):
    def __init__(self, dynamodb_table: str):
        self.table_name = dynamodb_table
        self.client = boto3.client('dynamodb')

    def _retrieve_raw(
            self, device: str, data_from: str, data_to: str, attributes: list | None = None
    ) -> dict:
        # querying specific attributes does not seem to be directly supported
        # - requires each attribute to be stored in a separate column
        # which seems to be problematic to achieve with IoT topic rule

        request_from = data_from
        request_to = data_to

        query_params = {
            "TableName": self.table_name,
            "Select": "ALL_ATTRIBUTES",
            "KeyConditionExpression": "device_id = :device_id AND #time BETWEEN :data_from AND :data_to",
            "ExpressionAttributeNames": {
                '#time': 'time'
            },
            "ExpressionAttributeValues": {
                ':device_id': {'S': device},
                ':data_from': {'S': request_from},
                ':data_to': {'S': request_to}
            }
        }

        err_count = 0
        err_count_total = 0
        requests_stats = []
        items = []

        start_time = time.time()
        while request_from < request_to:
            if err_count > 3:
                break

            try:
                request_query_start_time = time.time()
                query_params["ExpressionAttributeValues"][":data_from"]["S"] = request_from
                response = self.client.query(
                    **query_params
                )
                request_query_end_time = time.time()
                request_query_elapsed = request_query_end_time - request_query_start_time

                response_items = response['Items']

                items_length = len(response_items)


                stats = {
                    "elapsed": request_query_elapsed,
                    "request_from": request_from,
                    "request_to": request_to,
                    "items_length": items_length
                }

                if items_length > 0:
                    items.extend(response_items)

                    first_item = response_items[0]
                    last_item = response_items[-1]

                    first_item_time = first_item["time"]["S"]
                    last_item_time = last_item["time"]["S"]

                    stats["first_item_time"] = first_item_time
                    stats["last_item_time"] = last_item_time

                    last_item_time_date = datetime.strptime(last_item_time, DATE_TIME_FORMAT)
                    request_from = (last_item_time_date + timedelta(seconds=1)).strftime(DATE_TIME_FORMAT)

                requests_stats.append(stats)

                if items_length == 0:
                    break

            except Exception as e:
                err_count += 1
                err_count_total += 1
                time.sleep(err_count/10)
                print(e)
                continue

        end_time = time.time()

        elapsed_time = end_time - start_time

        return {
            "records": {
                "items": items
            },
            "stats": {
                "data_from": data_from,
                "data_to": data_to,
                "elapsed": elapsed_time,
                "requests": requests_stats
            }
        }

    def _format(self, raw_data: dict) -> list:
        items = raw_data["items"]

        processed = []

        for item in items:
            sample_data = item["sample_data"]["M"]
            parameters = {}

            for key in sample_data.keys():
                sample_data_data = sample_data[key]
                parameters[key] = sample_data_data[next(iter(sample_data_data))]
            processed.append(parameters)

        return processed
