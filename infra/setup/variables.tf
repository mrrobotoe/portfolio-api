variable "tf_state_bucket" {
  description = "Name of S3 bucket to store Terraform state file"
  default     = "devops-portfolio-api-app-tf-state"
}

variable "tf_state_lock_table" {
  description = "Name of DynamoDB table to store Terraform state lock"
  default     = "devops-portfolio-api-app-tf-lock"
}

variable "project" {
  description = "Name of the project"
  default     = "portfolio-app-api"
}

variable "contact" {
  description = "Contact information for the project"
  default     = "acm.holmes@outlook.com"
}