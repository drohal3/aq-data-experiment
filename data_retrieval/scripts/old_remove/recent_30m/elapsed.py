import matplotlib.pyplot as plt
import json
import statistics

data_dynamo = []
items_dynamo = []

with open('local/recent_30m/DynamoDBRetrieverV2_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        json_line = json.loads(line)
        data_dynamo.append(json_line["requests"][0]["response_stats"]["req_stats"][0]["elapsed"])
        items_dynamo.append(json_line["requests"][0]["response_stats"]["req_stats"][0]["items"])


data_kinesis = []
items_kinesis = []

with open('local/recent_30m/KinesisRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        json_line = json.loads(line)
        data_kinesis.append(json_line["requests"][0]["response_stats"]["elapsed"])
        items_kinesis.append(sum(json_line["requests"][0]["response_stats"]["response_lengths"]))
#
data_timestream = []
items_timestream = []
with open('local/recent_30m/TimestreamDBRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        json_line = json.loads(line)
        data_timestream.append(json_line["requests"][0]["response_stats"]["elapsed"])

        reqs = json_line["requests"][0]["response_stats"]["requests_stats"]

        r = 0
        for req in reqs:
            r += req["rows"]
        items_timestream.append(r)

#
print("DynamoDB median: ", statistics.median(data_dynamo))
print("Kinesis median: ", statistics.median(data_kinesis))
print("Timestream median: ", statistics.median(data_timestream))

print("DynamoDB items avg: ", statistics.mean(items_dynamo))
print("Kinesis items avg: ", statistics.mean(items_kinesis))
print("Timestream items avg: ", statistics.mean(items_timestream))

data = [
    data_dynamo,
    data_kinesis,
    data_timestream
]
# Create box plot
plt.boxplot(data)
plt.title("Retrieval time of 30m recent data")
plt.ylabel("seconds")
plt.xticks([1,
            2,
            3
            ], [
    "DynamoDB",
    "Kinesis Data Stream",
    "Timestream"
])
plt.show()
