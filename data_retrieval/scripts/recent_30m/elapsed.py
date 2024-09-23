import matplotlib.pyplot as plt
import json

data_dynamo = []

with open('local/recent_30m/DynamoDBRetrieverV2_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        json_line = json.loads(line)
        data_dynamo.append(json_line["requests"][0]["response_stats"]["req_stats"][0]["elapsed"])

data_kinesis = []
with open('local/recent_30m/KinesisRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        json_line = json.loads(line)
        data_kinesis.append(json_line["requests"][0]["response_stats"]["elapsed"])
#
data_timestream = []
with open('local/recent_30m/TimestreamDBRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        json_line = json.loads(line)
        data_timestream.append(json_line["requests"][0]["response_stats"]["elapsed"])
#
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
