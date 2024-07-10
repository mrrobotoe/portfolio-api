variable "prefix" {
  description = "Prefix for resources in AWS"
  default     = "paa"
}

variable "project" {
  description = "Project name for tagging resources"
  default     = "portfolio-app-api"
}

variable "contact" {
  description = "Contact information for the tagging resources"
  default     = "acm.holmes@outlook.com"
}

# variable "db_username" {
#   description = "Username for the portfolio app api database"
#   default     = "portfolioapp"
# }

# variable "db_password" {
#   description = "Password for the Terraform database"
# }