# from terraform.tfvars

# ---------- GCP resources ------------
variable "gcp_project_id" {
  type         = string
  description  = "GCP Project ID"
}

variable "gcp_region" {
  type         = string
  description  = "GCP region"
}

variable "dns_name" {
  type         = string
  description  = "DNS name"
}

variable "project_name" {
  type         = string
  description  = "Name of this service"
}

variable "cloud_function_source" {
  type         = string
  description  = "Path to the source code of Cloud Function"
}

variable "cloud_function_entry_point" {
  type         = string
  description  = "Name of Cloud Function entry point"
}

# ------------ Database ---------------
variable "db_name" {
  type         = string
  description  = "Database name"
}

variable "db_user_name" {
  type         = string
  description  = "Database user name"
}

variable "db_user_password" {
  type         = string
  description  = "Database user password"
  sensitive    = true
}


# ------------ Django -----------------
variable "django_debug_mode" {
  type         = string
  description  = "Flag to enable Django debug mode"
}

variable "django_secret_key" {
  type         = string
  description  = "SECRET_KEY of django app"
  sensitive    = true
}