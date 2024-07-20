# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_iam

resource "google_storage_bucket" "media_bucket" {
  name          = "${var.project_name}-media-bucket-${random_string.random.result}"
  project       = module.project_services.project_id
  location      = var.gcp_region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "static_bucket" {
  name          = "${var.project_name}-static-bucket-${random_string.random.result}"
  project       = module.project_services.project_id
  location      = var.gcp_region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "private_bucket" {
  name          = "${var.project_name}-private-bucket-${random_string.random.result}"
  project       = module.project_services.project_id
  location      = var.gcp_region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "media_bucket_public_rule" {
  bucket  = google_storage_bucket.media_bucket.name
  role    = "roles/storage.legacyObjectReader"
  members = [
    "allUsers",
  ]
  depends_on = [module.project_services]
}

resource "google_storage_bucket_iam_binding" "static_bucket_public_rule" {
  bucket  = google_storage_bucket.static_bucket.name
  role    = "roles/storage.legacyObjectReader"
  members = [
    "allUsers",
  ]
  depends_on = [module.project_services]
}

resource "google_storage_bucket_iam_binding" "private_bucket_rule" {
  bucket  = google_storage_bucket.private_bucket.name
  role    = "roles/storage.admin"
  members = [
    "serviceAccount:${google_service_account.custom_service_account_cf.email}"
  ]
  depends_on = [module.project_services]
}

resource "google_storage_bucket_object" "cloud_function_source_archive" {
  name   = "django-task.zip"
  bucket = google_storage_bucket.private_bucket.name
  source = data.archive_file.cloud_function_source.output_path
}