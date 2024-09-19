from .abstract_retriever import AbstractRetriever
from datetime import datetime, timedelta
import boto3
import json

STREAM_NAME = "aq-data-stream"
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class S3Retriever(AbstractRetriever):
    BUCKET = "idealaq-aq-measurements-bucket"

    def __init__(self):
        self.client = boto3.client('s3')

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None) -> dict:
        # key = "data/device_id=test_1/year:2024/month:09/day:07/hour:11/terraform-kinesis-firehose-extended-s3-test-stream-3-2024-09-07-11-21-19-13dbaf12-8ca8-3761-93dd-651fcf2e96ed"

        date_str = data_from

        contents = []
        while date_str <= data_to:
            print(date_str)
            date = datetime.strptime(date_str, DATE_TIME_FORMAT)
            next_date = date + timedelta(hours=1)

            prefix = f"data/device_id={device}/year:{date.year:04}/month:{date.month:02}/day:{date.day:02}/hour:{date.hour:02}/"
            print("prefix: ", prefix)
            response = self.client.list_objects_v2(
                Bucket=self.BUCKET,
                Delimiter='/',
                MaxKeys=1000,
                Prefix=prefix,
            )

            if "Contents" in response:
                contents.extend(response["Contents"])
            else:
                print(f"No Key for {date_str}'s hour")

            date_str = next_date.strftime(DATE_TIME_FORMAT)

        contents_list = []

        for content in contents:
            key = content["Key"]
            response = self.client.get_object(
                Bucket=self.BUCKET,
                Key=content['Key']
            )

            contents_list.append(response["Body"].read().decode('utf-8'))

        return {
            "records": {
                "files_contents": contents_list
            },
            "stats": {}
        }

    def _format(self, data: dict) -> list:
        items = []
        file_contents = data["files_contents"]

        for content in file_contents:
            lines = content.splitlines()
            for line in lines:
                json_line = json.loads(line)
                items.append(json_line)

        return items
