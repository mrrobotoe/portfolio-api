variable "tf_state_bucket" {
  description = "Name of S3 bucket in AWS for storing TF state"
  default     = "devops-portfolio-api-app-tf-state"
}

variable "tf_state_lock_table" {
  description = "Name of DynamoDB table for TF state locking"
  default     = "devops-portfolio-app-api-tf-lock"
}

variable "project" {
  description = "Project name for tagging resources"
  default     = "portfolio-app-api"
}

variable "contact" {
  description = "Contact name for tagging resources"
  default     = "acm.holmes@outlook.com"
}