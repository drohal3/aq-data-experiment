# AWS timeseries experiment

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

