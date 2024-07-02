from dotenv import dotenv_values
from awscrt import mqtt
from awsiot import mqtt_connection_builder
from datetime import datetime, timezone
import json
import time
import asyncio
import random


ENV_AWS_MQTT_ENDPOINT = "AWS_MQTT_ENDPOINT"
ENV_AWS_MQTT_CLIENT_ID = "AWS_MQTT_CLIENT_ID"
ENV_AWS_MQTT_CERTIFICATE_FILE = "AWS_MQTT_CERTIFICATE_FILE"
ENV_AWS_MQTT_PRIVATE_KEY_FILE = "AWS_MQTT_PRIVATE_KEY_FILE"
ENV_AWS_MQTT_ROOT_CA_FILE = "AWS_MQTT_ROOT_CA_FILE"
ENV_AWS_MQTT_PORT = "AWS_MQTT_PORT"

def _on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


def _on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(
        "Connection resumed. return_code: {} session_present: {}".format(
            return_code, session_present
        )
    )

class AWS_MQTT_Publisher:
    def __init__(self, endpoint, port, cert_file_path, private_key_path, ca_file_path, client_id) -> None:

        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=endpoint,
            port=port,
            cert_filepath=cert_file_path,  # --cert
            pri_key_filepath=private_key_path,  # --key
            ca_filepath=ca_file_path,  # --ca_file
            on_connection_interrupted=_on_connection_interrupted,
            on_connection_resumed=_on_connection_resumed,
            client_id=client_id,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None,
        )

        self.connect_future = self.mqtt_connection.connect()
        self.connect_future.result()
        print(f"Connecting to {endpoint} with client ID '{client_id}'...")
        print("Connected!")

    def publish(self, topic: str, data: dict):
        message_json = json.dumps(data)
        # Future.result() waits until a result is available

        self.mqtt_connection.publish(
            topic=topic, payload=message_json, qos=mqtt.QoS.AT_LEAST_ONCE
        )

        print(f"topic: {topic}, data: {data}")

    def close(self):
        print("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

async def simulate_device(publisher: AWS_MQTT_Publisher, device_id: str, step_time: int = 1, message_limit: int = -1):
    start_time = time.time()
    loops = 0
    previous_message = {}
    next_data = {}

    def run_step(message: dict):
        publisher.publish("cpc/main", message)

    def next_value(
            key: str,
            first_value: float,
            min_value: float,
            max_value: float,
            min_steps_trend: int = 1,
            max_steps_trend: int = 10
    ):
        previous_value = previous_message.get(key, first_value)
        next_data_setting = next_data.get("key", None)

        if next_data_setting is None:
            next_data_setting = {}

        steps = next_data_setting.get("steps", 0)
        step_change = next_data_setting.get("step_change", 0)
        if steps <= 0:
            steps = random.randint(min_steps_trend, max_steps_trend) + 1
            target_value = random.uniform(min_value, max_value)
            difference = target_value - previous_value
            step_change = difference / steps

        steps = steps - 1

        next_data[key] = {steps, step_change}
        return previous_value + step_change

    while loops != message_limit:
        loops = loops + 1
        loop_start_time = time.time()

        new_message = {
            "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "device_id": device_id,
            "temperature": next_value("temperature", 27.5, 27.0, 29.0, 1, 100),
            "humidity": next_value("humidity", 40, 35, 65, 1, 100),
            "pn": next_value("pn", 10000, 1000, 100000, 1, 20),
            "co": next_value("co", 3.5, 3, 5),
            "co2": next_value("co2", 420, 400, 500)
        }

        previous_message = new_message

        await asyncio.get_event_loop().run_in_executor(None, run_step, new_message)

        loop_end_time = time.time()
        loop_elapsed_time = loop_end_time - loop_start_time

        loop_sleep_time = step_time - loop_elapsed_time

        if loop_sleep_time < 0:
            print(f"elapsed time {loop_sleep_time} is larger than step time {step_time}!")
            loop_sleep_time = 0

        await asyncio.sleep(loop_sleep_time)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Simulation of device {device_id} finished after {elapsed_time} seconds!")


def main():
    env_config = dotenv_values()

    publisher = AWS_MQTT_Publisher(
        endpoint=env_config[ENV_AWS_MQTT_ENDPOINT],
        port=int(env_config[ENV_AWS_MQTT_PORT]),
        cert_file_path=env_config[ENV_AWS_MQTT_CERTIFICATE_FILE],
        private_key_path=env_config[ENV_AWS_MQTT_PRIVATE_KEY_FILE],
        ca_file_path=env_config[ENV_AWS_MQTT_ROOT_CA_FILE],
        client_id=env_config[ENV_AWS_MQTT_CLIENT_ID]
    )

    tasks = []
    print("creating devices...")
    devices = 3
    step_time = 1
    device_id_prefix = "9"
    message_limit = 5  # 300  # 5 minutes * 60 seconds = 300
    for i in range(devices):
        tasks.append(simulate_device(publisher, f"{device_id_prefix}{i}", step_time, message_limit))
    print(f"created {devices} devices!")

    print("simulating...")
    loop = asyncio.get_event_loop()
    start_time = time.time()
    loop.run_until_complete(asyncio.gather(*tasks))
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"elapsed time: {elapsed_time}")


if __name__ == '__main__':
    main()

