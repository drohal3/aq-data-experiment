from .abstract_retriever import AbstractRetriever
import boto3
import time

class TimestreamDBRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('timestream-query')

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: list | None = None) -> dict:
        start_time = time.time()

        value_string = ""
        if attributes is not None:
            value_string = ', '.join(f"'{value}'" for value in attributes)
        measurement_condition = "" if attributes is None else f"measure_name in ({value_string}) AND"

        query_string = f"""
            SELECT measure_name, time, measure_value::double
            FROM "aq-time-stream"."aq_data"
            WHERE {measurement_condition}
            device_id = '{device}'
            AND time >= '{data_from}.000000000' 
            AND time <= '{data_to}.000000000'
            ORDER BY time, measure_name
        """

        print("Query string:", query_string)

        requests_stats = []
        rows = []
        empty_rows = 0
        next_token = None
        while True:
            if empty_rows > 3:
                break
            get_records_start = time.time()
            response = self.client.query(QueryString=query_string) if next_token is None else self.client.query(QueryString=query_string, NextToken=next_token)
            get_records_end = time.time()
            rows_r = response['Rows']
            response_length = len(rows_r)
            if response_length == 0:
                empty_rows += 1
            else:
                empty_rows = 0
                rows.extend(rows_r)
            stats = {
                "get_records_start": get_records_start,
                "get_records_end": get_records_end,
                "get_records_elapsed": get_records_end - get_records_start,
                "rows": response_length,
            }

            requests_stats.append(stats)
            next_token = None if "NextToken" not in response else response["NextToken"]

            if next_token is None:
                break

        end_time = time.time()

        return {
            "records": {
                "rows": rows,
                "device_id": device
            },
            "stats": {
                "start_time": start_time,
                "end_time": end_time,
                "elapsed": end_time - start_time,
                "requests_stats": requests_stats,
                "requests": len(requests_stats)
            }
        }

    def _format(self, data: dict) -> list:
        # print("===> ===> ", data)
        # return []
        rows = data['rows']
        device_id = data['device_id']
        last_time = "-1"
        last_row = None
        processed = []

        # WARNING: the code below assumes the rows are sorted by time
        # WARNING: the code below assumes that only one device is queried
        # WARNING: the code below assumes that all values are floats/doubles
        for row in rows:
            data = row["Data"]
            data_time = data[1]["ScalarValue"][:19]
            if last_time != data_time:
                last_time = data_time
                if last_row is not None:
                    processed.append(last_row)
                last_row = {
                    "time": data_time,
                    "device_id": device_id
                }
            measure_name = data[0]["ScalarValue"]
            if measure_name == "device_id" or measure_name == "time":
                continue

            value = data[2]["ScalarValue"]
            last_row[measure_name] = value

        if last_row is not None:
            processed.append(last_row)

        return processed
