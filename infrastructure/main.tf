########################################################################################################################
########################################################################################################################
variable "region" {
  description = "The AWS region to deploy the resources"
  default     = "eu-central-1"
  type        = string
}

variable "iot_topic" {
  description = "The MQTT topic for IoT Core"
  default     = "aq/measurement"
  type        = string
}

variable "iot_topic_experiment" {
  description = "The MQTT topic for IoT Core"
  default     = "aq/experiment"
  type        = string
}

provider "aws" {
  region = var.region
}

#######################################################################################################################
#######################################################################################################################
## IoT Policy ====>
resource "aws_iot_policy" "aq_data_iot_core_policy" {
  name = "aq_data_iot_core_policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "iot:Publish",
          "iot:Receive"
        ],
        Effect = "Allow",
        Resource = [
          "arn:aws:iot:${var.region}:${data.aws_caller_identity.current.account_id}:topic/${var.iot_topic}",
          "arn:aws:iot:${var.region}:${data.aws_caller_identity.current.account_id}:topic/${var.iot_topic_experiment}",
          "arn:aws:iot:${var.region}:${data.aws_caller_identity.current.account_id}:topic/aq/test"
        ]
      },
      {
        Action = [
          "iot:Connect"
        ],
        Effect = "Allow",
        Resource = [
          "arn:aws:iot:${var.region}:${data.aws_caller_identity.current.account_id}:client/aq*Client",
        ]
      },
      {
        Action = [
          "iot:Subscribe"
        ],
        Effect = "Allow",
        Resource = [
          "arn:aws:iot:${var.region}:${data.aws_caller_identity.current.account_id}:topicfilter/${var.iot_topic}",
          "arn:aws:iot:${var.region}:${data.aws_caller_identity.current.account_id}:topicfilter/aq/test"
        ]
      }
      # Add more statements as needed for other permissions
    ]
  })
}

data "aws_caller_identity" "current" {}

# ### certificates
#######################################################################################################################
# Test Client
resource "aws_iot_thing" "iot_thing" {
  name = "MyIotThing"
}

resource "aws_iot_certificate" "iot_cert" {
  active = true
}

resource "aws_iot_policy_attachment" "iot_policy_attachment" {
  policy = aws_iot_policy.aq_data_iot_core_policy.name
  target = aws_iot_certificate.iot_cert.arn
}

resource "aws_iot_thing_principal_attachment" "iot_thing_attachment" {
  thing     = aws_iot_thing.iot_thing.name
  principal = aws_iot_certificate.iot_cert.arn
}

output "certificate_arn" {
  value = aws_iot_certificate.iot_cert.arn
}

output "certificate_pem" {
  value     = aws_iot_certificate.iot_cert.certificate_pem
  sensitive = true
}

output "private_key" {
  value     = aws_iot_certificate.iot_cert.private_key
  sensitive = true
}

output "public_key" {
  value     = aws_iot_certificate.iot_cert.public_key
  sensitive = true
}

#######################################################################################################################
#######################################################################################################################

variable "expected_devices" {
  description = "Expected number of devices publishing data per second."
  type        = number
  default     = 1 # Adjust as needed! <=== <=== <===
}

#######################################################################################################################
#######################################################################################################################

module "dynamodb_option_experiment" {
  source         = "./modules/dynamodb_option"
  iot_topic      = var.iot_topic_experiment
  write_capacity = var.expected_devices
  read_capacity = var.expected_devices
  table_name = "aq_measurements_experiment"
  tags = {
    app = "aq_data",
    flow = "dynamodb"
  }
  name = "experiment"
}

module "timestream_option" {
  source    = "./modules/timestream_option"
  iot_topic = var.iot_topic_experiment
  table_name = "aq_data"
  tags = {
    app = "aq_data",
    flow = "timestream"
  }
}

module "datastreams_option" {
  source    = "./modules/datastreams_option"
  iot_topic = var.iot_topic_experiment
  tags = {
    app = "aq_data",
    flow = "datastreams"
  }
}