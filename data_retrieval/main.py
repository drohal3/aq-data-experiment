from data_retrievers import TimestreamDBRetriever, DynamoDBRetriever, KinesisRetriever, S3Retriever
def main():
    device = "test_89"
    data_from = "2024-09-07 11:21:20"
    data_to = "2024-09-07 11:21:25"
    attributes = ("pn", "temperature", "humidity")

    # retriever_timestream = TimestreamDBRetriever()
    # retriever_timestream.retrieve(device, data_from, data_to, attributes, True)

    retriever_dynamodb = DynamoDBRetriever()
    data = retriever_dynamodb.retrieve(device, data_from, data_to, attributes, False)
    print(data)

    # retriever_kinesis = KinesisRetriever()
    # retriever_kinesis.retrieve(device, data_from, data_to, attributes, True)

    # retriever_s3 = S3Retriever()
    # retriever_s3.retrieve(device, data_from, data_to, attributes, True)


if __name__ == '__main__':
    main()
