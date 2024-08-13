from data_retrievers import TimestreamDBRetriever, DynamoDBRetriever
def main():
    device = "test_1"
    data_from = "2024-08-13 11:12:04"
    data_to = "2024-08-13 11:12:06"
    attributes = ("co", "temperature", "humidity")

    # retriever_timestream = TimestreamDBRetriever()
    # retriever_timestream.retrieve(device, data_from, data_to, attributes, True)

    retriever_dynamodb = DynamoDBRetriever()
    retriever_dynamodb.retrieve(device, data_from, data_to, attributes, True)


if __name__ == '__main__':
    main()
