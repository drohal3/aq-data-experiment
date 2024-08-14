from .abstract_retriever import AbstractRetriever
import boto3

def format_dynamodb_data(data: dict) -> list:
    items = data["Items"]

    for item in items:
        pass

    return [{}]

class DynamoDBRetriever(AbstractRetriever):
    def __init__(self):
        # TODO: use session?
        self.client = boto3.client('dynamodb')

    def retrieve(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None, raw: bool = True) -> dict:
        response = self.client.query(
            TableName="aq_measurements",
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
