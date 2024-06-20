# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster

data "google_client_config" "default" {}

resource "google_container_cluster" "project_container_cluster" {
  name     = "${var.project_name}-container-cluster"
  project  = module.project_services.project_id
  location = var.gcp_region
  node_locations = [
    "${var.gcp_region}-a"
  ]

  remove_default_node_pool = true
  initial_node_count       = 1

  deletion_protection = false 

  timeouts {
    create = "30m"
    update = "40m"
  }

  workload_identity_config {
    workload_pool = "${var.gcp_project_id}.svc.id.goog"
  }
}

resource "google_container_node_pool" "project_node_pool" {
  name       = "${var.project_name}-node-pool"
  location   = var.gcp_region
  cluster    = google_container_cluster.project_container_cluster.name
  node_count = 2

  autoscaling {
    min_node_count = 1
    max_node_count = 3
  }

  node_config {
    machine_type = "e2-medium"

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
    oauth_scopes    = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append"
    ]
  }
}