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

        get_records_start = time.time()
        response = self.client.query(QueryString=query_string)
        get_records_end = time.time()

        end_time = time.time()

        response["device_id"] = device

        return {
            "records": response,
            "stats": {
                "start_time": start_time,
                "end_time": end_time,
                "elapsed": end_time - start_time,
                "get_records_start": get_records_start,
                "get_records_end": get_records_end,
                "get_records_elapsed": get_records_end - get_records_start
            }
        }

    def _format(self, data: dict) -> list:
        rows = data['Rows']
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
