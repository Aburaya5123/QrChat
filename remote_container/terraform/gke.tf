
data "google_client_config" "default" {}

resource "google_container_cluster" "project_container_cluster" {
  name     = "${var.project_name}-container-cluster"
  project  = module.project_services.project_id
  location = var.gcp_region

  enable_autopilot = true
  networking_mode = "VPC_NATIVE"

  deletion_protection = false 
}