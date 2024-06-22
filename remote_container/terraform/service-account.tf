
resource "google_service_account" "custom_service_account" {
  account_id    = "custom-service-account"
  display_name  = "${var.project_name}-Service-Account"
  description   = "Used for deploy & django app"
}

resource "google_service_account" "custom_service_account_cf" {
  account_id    = "custom-service-account-cf"
  display_name  = "${var.project_name}-Service-Account-CF"
  description   = "Used for cloud function"
}

resource "google_project_iam_member" "csa_sql_admin" {
  project       = var.gcp_project_id
  role          = "roles/cloudsql.admin"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csa_secret_accessor" {
  project       = var.gcp_project_id
  role          = "roles/secretmanager.secretAccessor"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csa_artifact_registry_reader" {
  project       = var.gcp_project_id
  role          = "roles/artifactregistry.reader"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csa_storage_admin" {
  project       = var.gcp_project_id
  role          = "roles/storage.admin"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csa_publisher" {
  project       = var.gcp_project_id
  role          = "roles/pubsub.publisher"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csa_netadmin" {
  project       = var.gcp_project_id
  role          = "roles/compute.networkAdmin"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csa_secadmin" {
  project       = var.gcp_project_id
  role          = "roles/compute.securityAdmin"
  member        = "serviceAccount:${google_service_account.custom_service_account.email}"
}

resource "google_project_iam_member" "csacf_storage_admin" {
  project       = var.gcp_project_id
  role          = "roles/storage.admin"
  member        = "serviceAccount:${google_service_account.custom_service_account_cf.email}"
}

resource "google_project_iam_member" "csacf_token_creator" {
  project       = var.gcp_project_id
  role          = "roles/iam.serviceAccountTokenCreator"
  member        = "serviceAccount:${google_service_account.custom_service_account_cf.email}"
}


module "workload_identity_for_cluster" {
  source  = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"

  providers = {
    kubernetes = kubernetes.project_container_cluster
  }
  use_existing_gcp_sa = true

  name                = google_service_account.custom_service_account.account_id
  namespace           = "default"
  project_id          = var.gcp_project_id

  depends_on = [google_container_cluster.project_container_cluster]
}