import matplotlib.pyplot as plt
import json

data_dynamo = []

PATH = "local/recent_1m_spec_attr"

with open(f'{PATH}/DynamoDBRetriever_1m_attr.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(len(json_line["response_stats"]["query_requests"]))

data_kinesis = []
with open(f'{PATH}/KinesisRetriever_1m_attr.txt', 'r') as file:
    # Read each line in the file
    failed = 0
    total = 0

    for line in file:
        total += 1
        json_line = json.loads(line)

        get_record_requests_stats = json_line["response_stats"]["get_record_requests"]
        last_stat = get_record_requests_stats[-1]

        missed_request_when_failed = 0
        if last_stat["items_length"] == 0:
            missed_request_when_failed = 1
            failed += 1

        describe_streams_requests = 1
        get_shard_iterator_requests = 1
        get_record_requests = len(get_record_requests_stats) + missed_request_when_failed
        data_kinesis.append(describe_streams_requests + get_shard_iterator_requests + get_record_requests)

print(f"Failed kinesis: {failed} out of {total} = {failed / total * 100}%")

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever_1m_attr.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(len(json_line["response_stats"]["query_requests"]))

data = [data_dynamo, data_kinesis, data_timestream]
# Create box plot
plt.boxplot(data)
# plt.title("Retrieval time of 1m recent data")
plt.ylabel("number of requests")
plt.xticks([1, 2, 3], ["DynamoDB", "Kinesis Data Stream", "Timestream"])
plt.show()
