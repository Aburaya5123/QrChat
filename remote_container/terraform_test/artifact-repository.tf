# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/artifact_registry_repository

resource "google_artifact_registry_repository" "project-repository" {
  provider      = google-beta
  project       = module.project_services.project_id
  location      = var.gcp_region
  repository_id = "${var.project_name}-repository"
  description   = "Docker repository"
  format        = "DOCKER"
}
