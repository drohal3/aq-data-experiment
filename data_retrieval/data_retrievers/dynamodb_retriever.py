from .abstract_retriever import AbstractRetriever
import boto3
import time

class DynamoDBRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def _retrieve_raw(
            self, device: str, data_from: str, data_to: str, attributes: list | None = None
    ) -> dict:
        if attributes is not None:
            raise NotImplementedError

        start_time = time.time()

        response = self.client.query(
            TableName="aq_experiment",
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression='device_id = :device_id AND #time BETWEEN :data_from AND :data_to',
            ExpressionAttributeNames={
                '#time': 'time'
            },
            ExpressionAttributeValues={
                ':device_id': {'S': device},
                ':data_from': {'S': data_from},
                ':data_to': {'S': data_to}
            }
        )

        end_time = time.time()

        return {
            "records": response,
            "stats": {
                "start_time": start_time,
                "end_time": end_time,
                "elapsed": end_time - start_time
            }
        }

    def _format(self, raw_data: dict) -> list:
        items = raw_data["Items"]

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
