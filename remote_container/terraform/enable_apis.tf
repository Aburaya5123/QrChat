# https://github.com/terraform-google-modules/terraform-google-project-factory/tree/master/modules/project_services

module "project_services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  version                     = "~> 15.0"
  disable_services_on_destroy = true
  disable_dependent_services  = true
  project_id                  = var.gcp_project_id
  enable_apis                 = true
  activate_apis = [
    "compute.googleapis.com",# Compute API
    "cloudbuild.googleapis.com",# Cloud Build API
    "storage.googleapis.com",# Cloud Storage API
    "container.googleapis.com",# Kubernetes Engine API
    "artifactregistry.googleapis.com",# Artifact Registory
    "sqladmin.googleapis.com",# Cloud SQL Admin API
    "secretmanager.googleapis.com",# Secret Manager API
    "redis.googleapis.com",# Memorystore for Redis API
    "pubsub.googleapis.com",# PubSub API
    "cloudfunctions.googleapis.com",# Cloud Function API
    "eventarc.googleapis.com", # Event arc API (Cloud Function)
    "run.googleapis.com",# Cloud Run Admin API (Cloud Function)
    "cloudresourcemanager.googleapis.com",
  ]
}