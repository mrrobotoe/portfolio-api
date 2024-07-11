variable "prefix" {
  description = "Prefix for resources in AWS"
  default     = "raa"
}

variable "project" {
  description = "Project name for tagging resources"
  default     = "portfolio-app-api"
}

variable "contact" {
  description = "Contact email for tagging resources"
  default     = "acm.holmes@outlook.com"
}

variable "db_username" {
  description = "Username for the recipe app api database"
  default     = "portfolioapp"
}

variable "db_password" {
  description = "Password for the Terraform database"
}