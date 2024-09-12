# AWS timeseries experiment

Document is work in progress!

## IoT device simulator
Source code located in [device_simulation](./device_simulation)

to simulate devices:

- edit [.env](./device_simulation/.env) in [device_simulation](./device_simulation)
- define parameters in [parameters.yaml](./device_simulation/parameters.yaml) 
- run ```docker-compose up``` from [device_simulation](./device_simulation)
- wait for script to finish

```bash
docker-compose --file=./device_simulation/docker-compose.yml up 
```

## Data retrieval
Source code located in [data_retrieval](./data_retrieval)

The code in the repository intends to compare data retrieval from various data sources in AWS.
The experiment is conducted in Python with [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html) library.

> Please, refer to the official boto3 documentation regarding local configuration required to access AWS resources.
> [Official documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)

### DynamoDB
settings:
- provisioned capacity - it is assumed, the data loads will be predictable with no expected data bursts

observations:
- data can be queried using device_id (partition key) and time (sort key)
- in provisioned mode, write and read capacity must be adjusted


### Kinesis
settings:
- shard hash key is calculated from device_id using md5

observations:
- max 10000 items per request
- can't query items by device_id or timestamp... returns all content in the shard
- as consequence of the above two, the efficiency decreases by adding devices and number of items returned and needed to be filtered out increases which leads to the need for subsequent requests.
- requires multiple requests to find the correct shard - delays the request!

### S3

observations:
- complexity when used together with Kinesis - recent data must be retrieved from kinesis
- 
