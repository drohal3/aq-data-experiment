from .abstract_retriever import AbstractRetriever
from datetime import datetime, timedelta
import boto3
import json
import time

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class S3Retriever(AbstractRetriever):
    def __init__(self, s3_bucket: str):
        self.s3_bucket = s3_bucket
        self.client = boto3.client('s3')

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None) -> dict:
        # key = "data/device_id=test_1/year:2024/month:09/day:07/hour:11/terraform-kinesis-firehose-extended-s3-test-stream-3-2024-09-07-11-21-19-13dbaf12-8ca8-3761-93dd-651fcf2e96ed"
        start_time = time.time()
        date_str = data_from

        list_objects_requests_start = time.time()
        contents = []
        list_objects_requests = []
        while date_str <= data_to:
            # print(date_str)
            date = datetime.strptime(date_str, DATE_TIME_FORMAT)
            next_date = date + timedelta(hours=1)

            prefix = f"data/device_id={device}/year:{date.year:04}/month:{date.month:02}/day:{date.day:02}/hour:{date.hour:02}/"
            list_objects_request_start = time.time()
            response = self.client.list_objects_v2(
                Bucket=self.s3_bucket,
                Delimiter='/',
                MaxKeys=1000,
                Prefix=prefix,
            )
            list_objects_request_end = time.time()
            file_number = 0
            if "Contents" in response:
                contents.extend(response["Contents"])
                file_number = len(response["Contents"])
            else:
                print(f"No Key for {date_str}'s hour")

            date_str = next_date.strftime(DATE_TIME_FORMAT)

            list_objects_requests.append({
                "elapsed": list_objects_request_end - list_objects_request_start,
                "prefix": prefix,
                "file_number": file_number
            })

        list_objects_requests_end = time.time()

        get_object_requests_start = time.time()
        get_object_requests = []
        contents_list = []
        for content in contents:
            get_object_request_start = time.time()
            response = self.client.get_object(
                Bucket=self.s3_bucket,
                Key=content['Key']
            )
            get_object_request_end = time.time()

            contents_list.append(response["Body"].read().decode('utf-8'))
            get_object_requests.append({
                "elapsed": get_object_request_end - get_object_request_start,
                "key": content['Key']
            })

        end_time = get_object_requests_end = time.time()

        return {
            "records": {
                "files_contents": contents_list
            },
            "stats": {
                "data_from": data_from,
                "data_to": data_to,
                "elapsed": end_time - start_time,
                "list_objects_requests_elapsed": list_objects_requests_end - list_objects_requests_start,
                "list_objects_requests": list_objects_requests,
                "get_object_requests_elapsed": get_object_requests_end - get_object_requests_start,
                "get_object_requests": get_object_requests,
                "files_number": len(contents)
            }
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
