variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "endpoint" {
  description = "Where Terraform reaches the AWS API (Floci's port, 4566)"
  type        = string
  default     = "http://localhost:4566"
}

variable "lambda_endpoint" {
  description = "Where the Lambda container reaches Floci (localhost would mean the container itself)"
  type        = string
  default     = "http://host.docker.internal:4566"
}

variable "project" {
  description = "Short project name used in resource names"
  type        = string
  default     = "tasks"
}

variable "suffix" {
  description = "Added to every name, for example tf or dev"
  type        = string
  default     = "tf"
}

variable "stage_name" {
  description = "API Gateway stage"
  type        = string
  default     = "dev"
}