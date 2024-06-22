
resource "google_secret_manager_secret" "redis_host_ip" {
  project   = module.project_services.project_id
  secret_id = "REDIS_HOST_IP"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}

resource "google_secret_manager_secret" "static_bucket_name" {
  project   = module.project_services.project_id
  secret_id = "STATIC_BUCKET_NAME"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}

resource "google_secret_manager_secret" "media_bucket_name" {
  project   = module.project_services.project_id
  secret_id = "MEDIA_BUCKET_NAME"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}


resource "google_secret_manager_secret_version" "v_redis_host_ip" {
  secret        = google_secret_manager_secret.redis_host_ip.id
  secret_data   = google_redis_instance.memorystore_redis_instance.host
}

resource "google_secret_manager_secret_version" "v_static_bucket_name" {
  secret        = google_secret_manager_secret.static_bucket_name.id
  secret_data   = google_storage_bucket.static_bucket.name
}

resource "google_secret_manager_secret_version" "v_media_bucket_name" {
  secret        = google_secret_manager_secret.media_bucket_name.id
  secret_data   = google_storage_bucket.media_bucket.name
}


resource "google_secret_manager_secret_iam_binding" "binding_redis_host_ip" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.redis_host_ip.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}

resource "google_secret_manager_secret_iam_binding" "binding_static_bucket_name" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.static_bucket_name.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}

resource "google_secret_manager_secret_iam_binding" "binding_media_bucket_name" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.media_bucket_name.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}