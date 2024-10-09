import time

from .abstract_retriever import AbstractRetriever
import boto3
import hashlib
import json

# TODO: mention alternative https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html in thesis!

STREAM_NAME = "aq-data-stream"
LOOPS_EMPTY_LIMIT = 5

class KinesisRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('kinesis')

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None) -> dict:
        # WARNING: all data in the shard returned, not only with the ID
        start_time = time.time()
        # Compute MD5 hash of the partition key
        md5_hash = hashlib.md5(device.encode('utf-8')).hexdigest()

        # Convert MD5 hash (hex string) to an integer
        hash_key = int(md5_hash, 16)

        describe_stream_start = time.time()
        describe_stream = self.client.describe_stream(StreamName=STREAM_NAME)
        describe_stream_end = time.time()

        stream_arn = describe_stream["StreamDescription"]["StreamARN"]
        shards = describe_stream["StreamDescription"]["Shards"]

        shard_id_by_partition_key = 0

        for shard in shards:
            hash_range = shard["HashKeyRange"]
            if int(hash_range["StartingHashKey"]) <= hash_key <= int(hash_range["EndingHashKey"]):
                shard_id_by_partition_key = shard["ShardId"]
                break

        shard_iterator_start = time.time()
        shard_iterator = self.client.get_shard_iterator(
            StreamName=STREAM_NAME,
            ShardId=shard_id_by_partition_key,
            ShardIteratorType="AT_TIMESTAMP",
            Timestamp=data_from
        )
        shard_iterator_end = time.time()

        get_records_start = time.time()
        loops_empty = 0
        next_shard_iterator = shard_iterator["ShardIterator"]
        last_item_time = data_from

        items = []
        get_records_requests = []
        while last_item_time <= data_to:
            if loops_empty > LOOPS_EMPTY_LIMIT:
                break

            get_record_start = time.time()
            response = self.client.get_records(
                StreamARN=stream_arn,
                ShardIterator=next_shard_iterator,
            )
            get_record_end = time.time()

            next_shard_iterator = response["NextShardIterator"]
            response_items = response["Records"]
            response_items_length = len(response_items)

            stats = {
                "elapsed": get_record_end - get_record_start,
                "items_length": response_items_length,
            }

            if response_items_length > 0:
                loops_empty = 0
                first_item = response_items[0]
                last_item = response_items[-1]

                items.extend(response_items)

                first_item_time = json.loads(first_item["Data"].decode('utf-8'))["time"]
                last_item_time = json.loads(last_item["Data"].decode('utf-8'))["time"]

                stats["first_item_time"] = first_item_time
                stats["last_item_time"] = last_item_time
            else:
                loops_empty += 1

            get_records_requests.append(stats)

        end_time = get_records_end = time.time()

        return {
            "records": items,
            "stats": {
                "data_from": data_from,
                "data_to": data_to,
                "elapsed": end_time - start_time,
                "describe_stream_request_elapsed": describe_stream_end - describe_stream_start,
                "get_shard_iterator_elapsed": shard_iterator_end - shard_iterator_start,
                "get_records_request_elapsed": get_records_end - get_records_start,
                "get_record_requests": get_records_requests
            }
        }

    def _format(self, data_raw: dict) -> list:
        ret = []

        records = data_raw
        for record in records:
            record_data_b = record["Data"]
            json_str = record_data_b.decode('utf-8')
            data_dict = json.loads(json_str)
            ret.append(data_dict)
        return ret
