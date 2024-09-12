import time

from .abstract_retriever import AbstractRetriever
import boto3
import hashlib
import json

STREAM_NAME = "aq-data-stream"

class KinesisRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('kinesis')

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None) -> dict:
        # WARNING: all data in the shard returned, not only with the ID

        # Compute MD5 hash of the partition key
        md5_hash = hashlib.md5(device.encode('utf-8')).hexdigest()

        # Convert MD5 hash (hex string) to an integer
        hash_key = int(md5_hash, 16)

        describe_stream = self.client.describe_stream(StreamName=STREAM_NAME)
        # print(describe_stream)

        stream_arn = describe_stream["StreamDescription"]["StreamARN"]
        # print(stream_arn)

        shards = describe_stream["StreamDescription"]["Shards"]
        # print(shards)

        shard_id_by_partition_key = 0

        for shard in shards:
            hash_range = shard["HashKeyRange"]
            if int(hash_range["StartingHashKey"]) <= hash_key <= int(hash_range["EndingHashKey"]):
                shard_id_by_partition_key = shard["ShardId"]
                break

        print("shard_id_by_partition_key: ", shard_id_by_partition_key)

        shard_iterator = self.client.get_shard_iterator(
            StreamName=STREAM_NAME,
            ShardId=shard_id_by_partition_key,
            ShardIteratorType="LATEST"
        )

        records = self.client.get_records(
            StreamARN=stream_arn,
            ShardIterator=shard_iterator["ShardIterator"]
        )

        records_items = records["Records"]
        next_shard_iterator = records["NextShardIterator"]
        length = len(records_items)
        print("next_shard_iterator: ", next_shard_iterator)
        print("items number", length)

        if length == 0:
            print("No records")
            time.sleep(1)
            records = self.client.get_records(
                StreamARN=stream_arn,
                ShardIterator=next_shard_iterator
            )

        # NOTES: this option requires more extensive processing, the stream might contain old data if published with a delay (offline measurements)

        return records

    def _format(self, data_raw: dict) -> list:
        records = data_raw["Records"]
        for record in records:
            record_data_b = record["Data"]
            json_str = record_data_b.decode('utf-8')
            data_dict = json.loads(json_str)
            print(data_dict)
        return [{}]
