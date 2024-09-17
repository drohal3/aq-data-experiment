import time

from .abstract_retriever import AbstractRetriever
import boto3
import hashlib
import json
from datetime import timezone

# TODO: mention alternative https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html in thesis!

STREAM_NAME = "aq-data-stream"

class KinesisRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('kinesis', )

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

        loops_total = 0
        loop_empty_row_limit = 5
        loops_empty = 0
        loops_empty_total = 0
        response_lengths = []
        next_shard_iterator = shard_iterator["ShardIterator"]

        records_ret = []

        while True:
            loops_total += 1
            records = self.client.get_records(
                StreamARN=stream_arn,
                ShardIterator=next_shard_iterator
            )

            next_shard_iterator = records["NextShardIterator"]
            records_items = records["Records"]
            records_length = len(records_items)
            response_lengths.append(records_length)
            if records_length != 0:
                records_ret += records_items
                loops_empty = 0
                last_record = records_items[-1]
                dt = last_record["ApproximateArrivalTimestamp"]
                utc_dt_last_record = dt.astimezone(timezone.utc)
                utc_dt_last_record_str = utc_dt_last_record.strftime("%Y-%m-%d %H:%M:%S")

                if utc_dt_last_record_str <= data_to:
                    continue
            else:
                loops_empty += 1
                loops_empty_total += 1
                if loop_empty_row_limit > loops_empty:
                    continue
            break
        get_records_end = time.time()

        end_time = time.time()

        # NOTES: this option requires more extensive processing, the stream might contain old data if published with a delay (offline measurements)
        return {
            "records": records_ret,
            "stats": {
                "start_time": start_time,
                "end_time": end_time,
                "describe_stream_start": describe_stream_start,
                "describe_stream_end": describe_stream_end,
                "shard_iterator_start": shard_iterator_start,
                "shard_iterator_end": shard_iterator_end,
                "get_records_start": get_records_start,
                "get_records_end": get_records_end,
                "elapsed": end_time - start_time,
                "describe_stream_elapsed": describe_stream_end - describe_stream_start,
                "shard_iterator_elapsed": shard_iterator_end - shard_iterator_start,
                "get_records_elapsed": get_records_end - get_records_start,
                "get_requests": loops_total,
                "get_requests_empty": loops_empty_total,
                "response_lengths": response_lengths
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
