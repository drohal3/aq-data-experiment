import matplotlib.pyplot as plt
import statistics
import json
import statistics

PATH_A = "../local/arch_1d_all_attr"

data_dynamo_a = []
with open(f'{PATH_A}/DynamoDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo_a.append(json_line["response_stats"]["elapsed"])

data_s3_a = []
with open(f'{PATH_A}/S3Retriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_s3_a.append(json_line["response_stats"]["elapsed"])

data_timestream_a = []
with open(f'{PATH_A}/TimestreamDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream_a.append(json_line["response_stats"]["elapsed"])

PATH = "../local/arch_1d_spec_attr"

data_dynamo = []
with open(f'{PATH}/DynamoDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(json_line["response_stats"]["elapsed"])

data_s3 = []
with open(f'{PATH}/S3Retriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_s3.append(json_line["response_stats"]["elapsed"])

data_timestream = []
with open(f'{PATH}/TimestreamDBRetriever.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(json_line["response_stats"]["elapsed"])

data_a = [data_dynamo_a, data_s3_a, data_timestream_a]
data = [data_dynamo, data_s3, data_timestream]

# Create a figure with two subplots next to each other
fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)  # sharey=True keeps the y-axis consistent
FONT_SIZE_XTICK = 20

# Plot the first box plot on the first subplot
axs[0].boxplot(data_a)
axs[0].set_title("Full data items", fontsize=FONT_SIZE_XTICK)
axs[0].set_ylabel("seconds", fontsize=FONT_SIZE_XTICK*0.8)
axs[0].set_xticks([1, 2, 3])
axs[0].set_xticklabels(["Option 0\nDynamoDB", "Option 1\nS3", "Option 2\nTimestream"], fontsize=FONT_SIZE_XTICK)
axs[0].tick_params(axis="y", labelsize=FONT_SIZE_XTICK*0.9)


# Plot the second box plot on the second subplot
axs[1].boxplot(data)
axs[1].set_title("Specific parameter", fontsize=FONT_SIZE_XTICK)
axs[1].set_ylabel("seconds", fontsize=FONT_SIZE_XTICK*0.8)
axs[1].set_xticks([1, 2, 3])
axs[1].set_xticklabels(["Option 0\nDynamoDB", "Option 1\nS3", "Option 2\nTimestream"], fontsize=FONT_SIZE_XTICK)

# Show the plot
plt.tight_layout()
plt.show()
