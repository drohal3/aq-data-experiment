from .abstract_retriever import AbstractRetriever
import boto3
import hashlib

STREAM_NAME = "aq-data-stream"
def format_timestream_data(data: dict) -> list:
    return [{}]

class KinesisRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('kinesis')

    def retrieve(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None, raw: bool = True) -> dict:
        # shards = self.client.list_shards(StreamName="aq-data-stream")
        # print(shards)

        # Compute MD5 hash of the partition key
        md5_hash = hashlib.md5(device.encode('utf-8')).hexdigest()

        # Convert MD5 hash (hex string) to an integer
        hash_key = int(md5_hash, 16)

        print("hash key: ", hash_key)

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
            ShardIteratorType="TRIM_HORIZON"
        )

        # print(shard_iterator)

        # max 10000 records per call
        # can't query by device_id or timestamp

        records = self.client.get_records(
            StreamARN=stream_arn,
            ShardIterator=shard_iterator["ShardIterator"]
        )
        print(records)

        # NOTES: this option requires more extensive processing, the stream might contain old data if published with a delay (offline measurements)

        return {}
