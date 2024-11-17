DYNAMODB_TABLE = "aq_measurements_experiment"
S3_BUCKET = "idealaq-aq-measurements-bucket"
KINESIS_STREAM_NAME = "aq-data-stream"
TIMESTREAM_DATABASE = "aq-time-stream"
TIMESTREAM_TABLE = "aq_data"

def main():
    # you can import and run experiment script also from here!
    # you can also run a specific data retriever from here
    # and use describe_stats and describe_records for console print
    pass
def describe_stats(stats: dict):
    print("###################### stats ######################")
    for key in stats.keys():
        print(f"{key:<25}: {stats[key]}")
    print("###################################################")

def describe_records(records: list):
    for record in records:
        keys = record.keys()
        if "device_id" not in keys:
            continue

        if "time" not in keys:
            continue

        device_id = record["device_id"]
        time = record["time"]

        print(f"device_id: {device_id}, time: {time}")
        for key in keys:
            if key in ("time", "device_id"):
                continue
            print(f" {key:<15}: {record[key]}")


if __name__ == '__main__':
    main()
