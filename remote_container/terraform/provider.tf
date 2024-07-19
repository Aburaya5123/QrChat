
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.33.0"
    }
    google-beta = {
      source = "hashicorp/google-beta"
      version = "5.33.0"
    }
  }
  required_version = "=1.9.2"
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = "${var.gcp_region}-a"
}

provider "google-beta" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = "${var.gcp_region}-a"
}

provider "kubernetes" {
  alias                  = "project_container_cluster"
  host                   = "https://${google_container_cluster.project_container_cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.project_container_cluster.master_auth[0].cluster_ca_certificate)
}