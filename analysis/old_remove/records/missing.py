import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import statistics

DEVICES = 100

DYNAMO_DB_PREFIX = "DynamoDBRetrieverV2"
KINESIS_PREFIX = "KinesisRetriever"
TIMESTREAM_PREFIX = "TimestreamDBRetriever"

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def process(data_file: str, device_id: str):
    time_from = None
    time_to = None
    missing = []
    double = []
    expected_time = None
    line_number = 0
    with open(data_file, 'r') as file:
        for line in file:
            json_line = json.loads(line)
            line_device_id = json_line['device_id']
            if line_device_id != device_id:
                continue
            line_number += 1

            line_time = json_line["time"]

            # first line - set variables to initial state!
            if line_number == 1:
                time_from = line_time
                expected_time = line_time
            time_to = line_time
            while True:
                if line_number != 1:
                    time_d = datetime.strptime(expected_time, DATE_TIME_FORMAT)
                    expected_time = (time_d + timedelta(seconds=1)).strftime(DATE_TIME_FORMAT)

                if line_time > expected_time:
                    missing.append(expected_time)
                    continue

                if line_time < expected_time:
                    double.append(line_time)
                    expected_time = line_time
                    print(f"=====> ??? line time: {line_time}, expected time: {expected_time}, line number: {line_number} -- DOUBLE!")

                break

    time_from_d = datetime.strptime(time_from, DATE_TIME_FORMAT)
    time_to_d = datetime.strptime(time_to, DATE_TIME_FORMAT)
    seconds_expected = (time_to_d - time_from_d).total_seconds() + 1
    return {
        "time_from": time_from,
        "time_to": time_to,
        "seconds_expected": seconds_expected,
        "seconds_actual": line_number,
        "missing_percentage": 100 - ((line_number / seconds_expected) * 100),
        "missing": missing,
        "double": double,
        "missing_count": len(missing),
        "double_count": len(double)
    }


dynamo_missing_prc = []
kinesis_missing_prc = []
timestream_missing_prc = []

dynamo_missing_list = []
kinesis_missing_list = []
timestream_missing_list = []

for device_n in range(DEVICES):
    device = f"test_{device_n}"

    print(f"processing {device}, DynamoDB")
    dynamo_file = f"local/recent_30m/devices/{DYNAMO_DB_PREFIX}_{device}_30m.txt"
    stats_dynamo = process(dynamo_file, device)

    print(f"processing {device}, Kinesis")
    kinesis_file = f"local/recent_30m/devices/{KINESIS_PREFIX}_test_{device_n}_30m.txt"
    stats_kinesis = process(kinesis_file, device)

    print(f"processing {device}, Timestream")
    timestream_file = f"local/recent_30m/devices/{TIMESTREAM_PREFIX}_test_{device_n}_30m.txt"
    stats_timestream = process(timestream_file, device)

    dynamo_missing_prc.append(stats_dynamo["missing_percentage"])
    kinesis_missing_prc.append(stats_kinesis["missing_percentage"])
    timestream_missing_prc.append(stats_timestream["missing_percentage"])

print("\nDynamoDB:")
print(f" median: {statistics.median(dynamo_missing_prc)}")
print(f" mean: {statistics.mean(dynamo_missing_prc)}")

print("\nKinesis:")
print(f" median: {statistics.median(kinesis_missing_prc)}")
print(f" mean: {statistics.mean(kinesis_missing_prc)}")


print("\nTimestream:")
print(f" median: {statistics.median(timestream_missing_prc)}")
print(f" mean: {statistics.median(timestream_missing_prc)}")


data = [
    dynamo_missing_prc,
    kinesis_missing_prc,
    timestream_missing_prc
]
# Create box plot
plt.boxplot(data)
plt.title("Data loss rate")
plt.ylabel("percent")
plt.xticks([1,
            2,
            3
            ], [
    "DynamoDB",
    "Kinesis Data Stream",
    "Timestream"
])
plt.show()


#     dynamo_missing = stats_dynamo["missing"]
#     kinesis_missing = stats_kinesis["missing"]
#     timestream_missing = stats_timestream["missing"]
#
#     missing_merged = dynamo_missing + kinesis_missing + timestream_missing
#
#     for missing in set(missing_merged):
#         missing_count = missing_merged.count(missing)
#
#         if missing_count < 3:
#             print("Some Item is missing!!!!")
#             if missing in dynamo_missing and stats_dynamo["time_from"] <= missing <= stats_dynamo["time_to"]:
#                 print("missing in DynamoDB")
#                 dynamo_missing_list.append({
#                     "device": device,
#                     "time": missing,
#                     "double": stats_dynamo["double"]
#                 })
#
#             if missing in kinesis_missing and stats_kinesis["time_from"] <= missing <= stats_kinesis["time_to"]:
#                 print("missing in Kinesis")
#                 kinesis_missing_list.append(
#                     {
#                         "device": device,
#                         "time": missing,
#                         "double": stats_kinesis["double"]
#                     }
#                 )
#
#             if missing in timestream_missing and stats_timestream["time_from"] <= missing <= stats_timestream["time_to"]:
#                 print("missing in Timestream")
#                 timestream_missing_list.append(
#                     {
#                         "device": device,
#                         "time": missing,
#                         "double": stats_timestream["double"]
#                     }
#                 )
#
#     # print("dynamo", stats_dynamo)
#     # print("kinesis", stats_kinesis)
#     # print("timestream", stats_timestream)
#
# print(dynamo_missing_list)
# print(kinesis_missing_list)
# print(timestream_missing_list)