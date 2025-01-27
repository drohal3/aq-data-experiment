import matplotlib.pyplot as plt
import statistics
import json
import statistics

PATH = "../local/arch_1d_all_attr"

data_dynamo = []
with open(f'{PATH}/DynamoDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(json_line["response_stats"]["elapsed"])

print(f"Dynamo median: {statistics.median(data_dynamo)}")

data_s3 = []
with open(f'{PATH}/S3Retriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_s3.append(json_line["response_stats"]["elapsed"])

print(f"S3 median: {statistics.median(data_s3)}")
print(f"S3 quantiles low: {statistics.quantiles(data_s3)}")

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(json_line["response_stats"]["elapsed"])

print(f"Timestream median: {statistics.median(data_timestream)}")


data = [data_dynamo, data_s3, data_timestream]
# Create box plot
plt.boxplot(data)
# plt.title("Retrieval time of 1d historical data")
plt.ylabel("seconds")
plt.xticks([1, 2, 3], ["Option 0\nDynamoDB", "Option 1\nS3", "Option 2\nTimestream"])
plt.show()
