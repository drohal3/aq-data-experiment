# Device simulation
## Prerequisite
Installed docker and docker-compose.

## Configuration
### ENV variables
> you can use [.env.sample](./.env.sapmle) file as template with `cp .env.sample .env` in [device_simulation](.) root directory

| variable                  |                     description                     |                                              example |
|---------------------------|:---------------------------------------------------:|-----------------------------------------------------:|
| AWS_MQTT_ENDPOINT         |                                                     |                     <???>.eu-central-1.amazonaws.com |
| AWS_MQTT_CLIENT_ID        |                                                     |                                           testClient |
| AWS_MQTT_CERTIFICATE_FILE |        device certificate file from AWS path        | /app/local/connect_device_package/deviceCert.crt.pem |
| AWS_MQTT_PRIVATE_KEY_FILE |          device private key from AWS path           |     /app/local/connect_device_package/privateKey.key |
| AWS_MQTT_ROOT_CA_FILE     |                    CA file path                     |        /app/local/connect_device_package/root-CA.crt |
| AWS_MQTT_PORT             |                      MQTT port                      |                                                 8883 |
| MQTT_TOPIC                |                     MQTT topic                      |                                      test/experiment |
| DEVICE_ID_PREFIX          |            prefix for device identifier             |                                                test_ |
| STEP_TIME                 |                step time in seconds                 |                                                    1 |
| DEVICES                   |             number of simulated devices             |                                                  100 |
| MESSAGE_LIMIT             | maximum number of simulated measurements per device |                                               100000 |

## Instructions
- create `local` directory in [device_simulation](.) rood directory
- place IoT device certificates in the directory ([tutorial](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html))
- configure .env file
- define parameters in [parameters.yaml](./parameters.yaml)
- run `docker-compose up` from [device_simulation](.) root directory

> for longer experiments, you might consider to provision an EC2 instance from AWS 

> Please, refer to the official boto3 documentation regarding local configuration required to access AWS resources.
> [Official documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
