# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_user

resource "google_sql_database" "database" {
  name             = var.db_name
  instance         = google_sql_database_instance.instance.name
}

resource "google_sql_database_instance" "instance" {
  name             = "${var.project_name}-database-instance"
  project          = module.project_services.project_id
  region           = var.gcp_region
  database_version = "MYSQL_8_0"
  settings {
    tier = "db-f1-micro"
  }

  deletion_protection  = "false"
}

resource "google_sql_user" "users" {
  name             = var.db_user_name
  instance         = google_sql_database_instance.instance.name
  password         = var.db_user_password
}