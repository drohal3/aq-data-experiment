from .abstract_retriever import AbstractRetriever
import boto3

class DynamoDBRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def _retrieve_raw(
            self, device: str, data_from: str, data_to: str, attributes: tuple | None = None
    ) -> dict:
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
        print(response)
        return {}

    def _format(self, raw_data) -> list:
        items = raw_data["Items"]

        for item in items:
            pass

        return [{}]
