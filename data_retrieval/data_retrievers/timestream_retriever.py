from .abstract_retriever import AbstractRetriever
import boto3
class TimestreamDBRetriever(AbstractRetriever):
    def __init__(self):
        self.client = boto3.client('timestream-query')

    def retrieve(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None, raw: bool = True) -> dict:
        value_string = ""
        if attributes is not None:
            value_string = ', '.join(f"'{value}'" for value in attributes)
        measurement_condition = "" if attributes is None else f"WHERE measure_name in ({value_string})"

        query_string = f"""
            SELECT measure_name, time, measure_value::double
            FROM "aq-time-stream"."aq_data"
            {measurement_condition}
            AND device_id = '{device}'
            AND time >= '{data_from}.000000000' 
            AND time <= '{data_to}.000000000'
            ORDER BY time, measure_name
        """

        print(query_string)

        response = self.client.query(QueryString=query_string)
        ret = {}

        if raw is True:
            ret["response"] = response
            return ret

        rows = response['Rows']

        last_time = "-1"
        last_row = None
        processed = []

        # WARNING: the code below assumes the rows are sorted by time
        # WARNING: the code below assumes that only one device is queried
        for row in rows:
            data = row["Data"]
            time = data[1]["ScalarValue"][:19]
            if last_time != time:
                last_time = time
                if last_row is not None:
                    processed.append(last_row)
                last_row = {"time": time}
            measure_name = data[0]["ScalarValue"]
            value = data[2]["ScalarValue"]
            last_row[measure_name] = value

        return {"response": processed}

