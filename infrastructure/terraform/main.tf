terraform {
  required_version = ">= 1.7.0"
}

variable "project" { default = "nyayagpt" }

output "deployment_notes" {
  value = "Provision managed PostgreSQL, Redis, object storage, Kubernetes, secret manager, and observability stack for ${var.project}."
}
