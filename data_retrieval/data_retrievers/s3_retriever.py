from .abstract_retriever import AbstractRetriever
import boto3

STREAM_NAME = "aq-data-stream"
def format_s3_data(data: dict) -> list:
    return [{}]

class S3Retriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('s3')

    def retrieve(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None, raw: bool = True) -> dict:
        return {}
