https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

to simulate devices:

- edit [.env](./device_simulation/.env) in [device_simulation](./device_simulation)
- run ```docker-compose up``` from [device_simulation](./device_simulation)
- wait for script to finish

```bash
docker-compose --file=./device_simulation/docker-compose.yml up 
```