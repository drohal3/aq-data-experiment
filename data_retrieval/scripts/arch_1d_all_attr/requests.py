import matplotlib.pyplot as plt
import json
import statistics

data_dynamo = []

PATH = "local/arch_1d_all_attr"

with open(f'{PATH}/DynamoDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(len(json_line["response_stats"]["query_requests"]))

data_kinesis = []
with open(f'{PATH}/S3Retriever.txt', 'r') as file:
    # Read each line in the file
    failed = 0
    total = 0

    for line in file:
        total += 1
        json_line = json.loads(line)

        stats = json_line["response_stats"]
        list_object_requests = len(stats["list_objects_requests"])
        get_object_requests = len(stats["get_object_requests"])

        data_kinesis.append(list_object_requests + get_object_requests)

print(f"Failed kinesis: {failed} out of {total} = {failed/total*100}%")

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(len(json_line["response_stats"]["query_requests"]))

print(f"DynamoDB: {statistics.median(data_dynamo)}")
print(f"S3: {statistics.quantiles(data_kinesis)}")
print(f"Timestream: {statistics.median(data_timestream)}")



data = [data_dynamo, data_kinesis, data_timestream]
# Create box plot
plt.boxplot(data)
# plt.title("Retrieval time of 1m recent data")
plt.ylabel("number of requests")
plt.xticks([1, 2, 3], ["DynamoDB", "S3", "Timestream"])
plt.show()
