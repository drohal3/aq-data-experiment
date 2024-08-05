from .abstract_retriever import AbstractRetriever
import boto3
class DynamoDBRetriever(AbstractRetriever):
    def retrieve(self, device: str, data_from: str, data_to: str) -> dict:
        pass
