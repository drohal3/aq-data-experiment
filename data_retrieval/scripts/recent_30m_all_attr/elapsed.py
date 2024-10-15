import matplotlib.pyplot as plt
import json

data_dynamo = []

PATH = "local/recent_30m_all_attr"

with open(f'{PATH}/DynamoDBRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(json_line["response_stats"]["elapsed"])

data_kinesis = []
with open(f'{PATH}/KinesisRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_kinesis.append(json_line["response_stats"]["elapsed"])

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever_30m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(json_line["response_stats"]["elapsed"])

data = [data_dynamo, data_kinesis, data_timestream]
# Create box plot
plt.boxplot(data)
plt.title("Retrieval time of 30m recent data")
plt.ylabel("seconds")
plt.xticks([1, 2, 3], ["DynamoDB", "Kinesis Data Stream", "Timestream"])
plt.show()
