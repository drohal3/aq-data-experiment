from data_retrievers import TimestreamDBRetriever, DynamoDBRetriever, KinesisRetriever, S3Retriever
from experiments import recent_1m, recent_1m_spec_attr, recent_30m, recent_30m_spec_attr, arch_1d, arch_1d_spec_attr
# from experiments import recent_data_30m, arch_data_1h, recent_data_1m_v2
import json

DYNAMODB_TABLE = "aq_measurements_experiment"
S3_BUCKET = "idealaq-aq-measurements-bucket"
KINESIS_STREAM_NAME = "aq-data-stream"
TIMESTREAM_DATABASE = "aq-time-stream"
TIMESTREAM_TABLE = "aq_data"

def main():
    device = "test_00"
    data_from = "2024-10-09 16:30:11"
    data_to = "2024-10-09 16:30:25"
    attributes = ["key00"]

    arch_1d.run_experiment()
    # attributes = None

    # recent_data_1m_v2.run_experiment()

    # recent_data_30m.run_experiment()

    # arch_data_1h.run_experiment()

    # retriever_timestream = TimestreamDBRetriever(TIMESTREAM_DATABASE, TIMESTREAM_TABLE)
    # data = retriever_timestream.retrieve(device, data_from, data_to, attributes, False)

    # retriever_dynamodb = DynamoDBRetriever(DYNAMODB_TABLE)
    # data = retriever_dynamodb.retrieve(device, data_from, data_to, attributes, False)

    # retriever_kinesis = KinesisRetriever()
    # data = retriever_kinesis.retrieve(device, data_from, data_to, None, False)

    # retriever_s3 = S3Retriever(S3_BUCKET)
    # data = retriever_s3.retrieve(device, data_from, data_to, attributes, False)

    # ####################################
    # print
    # describe_records(data["records"])
    # describe_stats(data["stats"])

def describe_stats(stats: dict):
    print("###################### stats ######################")
    for key in stats.keys():
        print(f"{key:<25}: {stats[key]}")
    print("###################################################")

def describe_records(records: list):
    for record in records:
        keys = record.keys()
        if "device_id" not in keys:
            continue

        if "time" not in keys:
            continue

        device_id = record["device_id"]
        time = record["time"]

        print(f"device_id: {device_id}, time: {time}")
        for key in keys:
            if key in ("time", "device_id"):
                continue
            print(f" {key:<15}: {record[key]}")


if __name__ == '__main__':
    main()
