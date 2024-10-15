from .abstract_retriever import AbstractRetriever
import boto3
import time

class TimestreamDBRetriever(AbstractRetriever):
    def __init__(self, database: str, table: str):
        self.client = boto3.client('timestream-query')
        self.database = database
        self.table = table

    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: list | None = None) -> dict:
        start_time = time.time()

        value_string = ""
        if attributes is not None:
            value_string = ', '.join(f"'{value}'" for value in attributes)
        measurement_condition = "" if attributes is None else f"measure_name in ({value_string}) AND"

        query_string = f"""
            SELECT measure_name, time, measure_value::double
            FROM "{self.database}"."{self.table}"
            WHERE {measurement_condition}
            device_id = '{device}'
            AND time >= '{data_from}.000000000' 
            AND time <= '{data_to}.000000000'
            ORDER BY time, measure_name
        """

        query_requests = []
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
            row_stats = {}
            if response_length == 0:
                empty_rows += 1
            else:
                empty_rows = 0
                rows.extend(rows_r)

                first_row = rows_r[0]
                last_row = rows_r[-1]

                row_stats["first_item_time"] = first_row["Data"][1]["ScalarValue"][:19]
                row_stats["last_item_time"] = last_row["Data"][1]["ScalarValue"][:19]

            query_requests.append({
                "get_records_elapsed": get_records_end - get_records_start,
                "item_number": response_length,
                **row_stats
            })

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
                "data_from": data_from,
                "data_to": data_to,
                "elapsed": end_time - start_time,
                "query_requests": query_requests,
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
