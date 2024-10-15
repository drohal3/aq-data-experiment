import matplotlib.pyplot as plt
import statistics
import json
import statistics

PATH = "local/recent_1m_all_attr"

data_dynamo = []
with open(f'{PATH}/DynamoDBRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(json_line["response_stats"]["elapsed"])

print(f"Dynamo median: {statistics.median(data_dynamo)}")

data_kinesis = []
with open(f'{PATH}/KinesisRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_kinesis.append(json_line["response_stats"]["elapsed"])

print(f"Kinesis median: {statistics.median(data_kinesis)}")
print(f"Kinesis quantiles low: {statistics.quantiles(data_kinesis)}")

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(json_line["response_stats"]["elapsed"])

print(f"Timestream median: {statistics.median(data_timestream)}")


data = [data_dynamo, data_kinesis, data_timestream]
# Create box plot
plt.boxplot(data)
plt.title("Retrieval time of 1m recent data")
plt.ylabel("seconds")
plt.xticks([1, 2, 3], ["DynamoDB", "Kinesis Data Stream", "Timestream"])
plt.show()
