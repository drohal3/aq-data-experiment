import matplotlib.pyplot as plt
import json

data_kinesis = []
data_kinesis_no_zero = []

with open('local/recent_1m/KinesisRetriever_1m.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip newline characters and print each line
        json_line = json.loads(line)
        n = len(json_line["response_stats"]["response_lengths"])
        z = json_line["response_stats"]["get_requests_empty"]
        if n == 7 and z == 5:
            n += 1
        data_kinesis.append(n)
        data_kinesis_no_zero.append(n - z)


# Create subplots (1 row, 2 columns)

# # plot with zeros
# bins = [1, 2, 3, 4, 5, 6, 7, 8]
#
#
# # Plot histogram on the second subplot
# plt.hist(data_kinesis, bins=bins, color='gray', edgecolor='black', align="left")
# # axes[0].set_title('Kinesis Data Stream')
# plt.xlabel('Number of requests per Kinesis Data Stream Query')
# plt.ylabel('percent')
# plt.ylim(0, 100)
#
#
# # Adjust spacing between plots
# plt.tight_layout()
#
# # Show the plot
# plt.show()





# # plot without zeros

bins = [0, 1, 2, 3, 4, 5]

# data adjustment after visual inspection:


# Plot histogram on the second subplot
plt.hist(data_kinesis_no_zero, bins=bins, color='gray', edgecolor='black', align="left")
# axes[0].set_title('Kinesis Data Stream')
plt.xlabel('Number of requests with non-empty response per Kinesis Data Stream Query')
plt.ylabel('percent')
plt.ylim(0, 100)


# Adjust spacing between plots
plt.tight_layout()

# Show the plot
plt.show()
