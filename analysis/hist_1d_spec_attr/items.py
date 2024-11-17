import matplotlib.pyplot as plt
import statistics
import json
import statistics

PATH = "local/arch_1d_all_attr"

data_dynamo = []
with open(f'{PATH}/DynamoDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(json_line["records_length"])

data_kinesis = []
with open(f'{PATH}/S3Retriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_kinesis.append(json_line["records_length"])

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(json_line["records_length"])

print(f"DynamoDB median length: {statistics.quantiles(data_dynamo)}")
print(f"S3 median length: {statistics.quantiles(data_kinesis)}")
print(f"Timestream median length: {statistics.quantiles(data_timestream)}")




# data = [data_dynamo, data_kinesis, data_timestream]
# # Create box plot
# plt.boxplot(data)
# plt.title("Record lengths")
# plt.ylabel("seconds")
# plt.xticks([1, 2, 3], ["DynamoDB", "Kinesis Data Stream", "Timestream"])
# plt.show()
