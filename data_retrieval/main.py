from data_retrievers import TimestreamDBRetriever, DynamoDBRetriever, KinesisRetriever, S3Retriever
from experiments import recent_data
def main():
    device = "test_0"
    data_from = "2024-09-17 11:22:30"
    data_to = "2024-09-17 11:22:39"
    attributes = ["time", "key01", "key02", "key14"]

    # recent_data.run_experiment()

    retriever_timestream = TimestreamDBRetriever()
    data = retriever_timestream.retrieve(device, data_from, data_to, None, False)

    # retriever_dynamodb = DynamoDBRetriever()
    # data = retriever_dynamodb.retrieve(device, data_from, data_to, None, False)

    # retriever_kinesis = KinesisRetriever()
    # data = retriever_kinesis.retrieve(device, data_from, data_to, None, False)

    # retriever_s3 = S3Retriever()
    # retriever_s3.retrieve(device, data_from, data_to, attributes, True)

    # ####################################
    # print
    describe_records(data["records"])
    describe_stats(data["stats"])

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
