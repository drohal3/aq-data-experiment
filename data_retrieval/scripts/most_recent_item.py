import matplotlib.pyplot as plt
import json

# Generate random data for two distributions
data_dynamo = []
with open('local/recent_1m/DynamoDBRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_dynamo.append(json_line["latest_item_delta"])

data_kinesis = []
with open('local/recent_1m/KinesisRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_kinesis.append(json_line["latest_item_delta"])

data_timestream = []
with open('local/recent_1m/TimestreamDBRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        data_timestream.append(json_line["latest_item_delta"])

# Create subplots (1 row, 2 columns)
fig, axes = plt.subplots(1, 3, figsize=(12, 5))

bins = [-2, -1, 0, 1, 2]


# Plot histogram on the first subplot
axes[0].hist(data_dynamo, bins=bins, color='gray', edgecolor='black')
axes[0].set_title('DynamoDB')
axes[0].set_xlabel('seconds delta')
axes[0].set_ylabel('percent')

# Plot histogram on the second subplot
axes[1].hist(data_kinesis, bins=bins, color='gray', edgecolor='black')
axes[1].set_title('Kinesis Data Stream')
axes[1].set_xlabel('seconds delta')
axes[1].set_ylabel('percent')

# Plot histogram on the second subplot
axes[2].hist(data_timestream, bins=bins, color='gray', edgecolor='black')
axes[2].set_title('Timestream')
axes[2].set_xlabel('seconds delta')
axes[2].set_ylabel('percent')

# Adjust spacing between plots
plt.tight_layout()

# Show the plot
plt.show()
