# Infrastructure for air quality data ingestion, storing and serving

## Preconditions
Logged in AWS CLI

## Instructions
- modify expected_devices variable in main.tf file (i.e. 100 devices)
- run terraform commands: fmt, init, plan and then apply

## Useful commands
format terraform files
```bash
terraform fmt
```

init terraform
```bash
terraform init
```

plan - prints changes to be done
```bash
terraform plan
```

apply changes
```bash
terraform apply
```

destroy infrastructure
```bash
terraform destroy
```

## Example data
...to be published to aq/measurement topic.
```JSON
{
  "time": "2024-04-15T16:45:12Z",
  "device_id": "cpc1",
  "temp_c": 0,
  "co_ppb": 0,
  "humidity_pct": 50,
  "saturator_temp_c": 0
}
```

to get IoT thing certificates, run
> **DANGER:** handle certificates with caution 
```bash
./scripts/outputsensitive.sh
```
