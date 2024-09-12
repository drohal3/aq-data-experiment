from .abstract_retriever import AbstractRetriever
import boto3

STREAM_NAME = "aq-data-stream"

class S3Retriever(AbstractRetriever):
    BUCKET = "idealaq-aq-measurements-bucket"

    def __init__(self):
        self.client = boto3.client('s3')

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None) -> dict:
        key = "data/device_id=test_1/year:2024/month:09/day:07/hour:11/terraform-kinesis-firehose-extended-s3-test-stream-3-2024-09-07-11-21-19-13dbaf12-8ca8-3761-93dd-651fcf2e96ed"
        # TODO: download every hour in requested range

        self.client.download_file(self.BUCKET, key, '/tmp/hello.txt')

        return {}

    def _format(self, data: dict) -> list:
        return [{}]
