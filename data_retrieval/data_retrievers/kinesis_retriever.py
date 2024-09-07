from .abstract_retriever import AbstractRetriever
import boto3

STREAM_NAME = "aq-data-stream"
def format_timestream_data(data: dict) -> list:
    return [{}]

class KinesisRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('kinesis')

    def retrieve(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None, raw: bool = True) -> dict:
        # shards = self.client.list_shards(StreamName="aq-data-stream")
        # print(shards)

        describe_stream = self.client.describe_stream(StreamName=STREAM_NAME)
        # print(describe_stream)

        stream_arn = describe_stream["StreamDescription"]["StreamARN"]
        # print(stream_arn)

        shards = describe_stream["StreamDescription"]["Shards"]
        shard_ids = [shard["ShardId"] for shard in shards]
        # print(shard_ids)

        shard_iterator = self.client.get_shard_iterator(
            StreamName=STREAM_NAME,
            ShardId=shard_ids[0],
            ShardIteratorType="TRIM_HORIZON"
        )

        # print(shard_iterator)

        records = self.client.get_records(
            StreamARN=stream_arn,
            ShardIterator=shard_iterator["ShardIterator"]
        )
        print(records)

        # NOTES: this option requires more extensive processing, the stream might contain old data if published with a delay (offline measurements)

        return {}
