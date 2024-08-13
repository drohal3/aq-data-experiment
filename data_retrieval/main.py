from data_retrievers import TimestreamDBRetriever
def main():
    device = "test_1"
    data_from = "2024-08-13 11:12:04"
    data_to = "2024-08-13 11:12:06"
    attributes = ("co", "temperature", "humidity")

    retriever = TimestreamDBRetriever()
    retriever.retrieve(device, data_from, data_to, attributes, False) # TODO: raw => True!!!


if __name__ == '__main__':
    main()
