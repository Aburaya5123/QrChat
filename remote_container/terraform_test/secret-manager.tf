# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/secret_manager_secret

resource "google_secret_manager_secret" "project_id" {
  project   = module.project_services.project_id
  secret_id = "PROJECT_ID"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}

resource "google_secret_manager_secret" "django_secret" {
  project   = module.project_services.project_id
  secret_id = "DJANGO_SECRET"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "django" }
}

resource "google_secret_manager_secret" "database_name" {
  project   = module.project_services.project_id
  secret_id = "DATABASE_NAME"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}

resource "google_secret_manager_secret" "database_user_name" {
  project   = module.project_services.project_id
  secret_id = "DATABASE_USER_NAME"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}

resource "google_secret_manager_secret" "database_user_password" {
  project   = module.project_services.project_id
  secret_id = "DATABASE_USER_PASSWORD"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}

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

resource "google_secret_manager_secret" "reserved_ip" {
  project   = module.project_services.project_id
  secret_id = "RESERVED_IP"
  replication {
    user_managed {
        replicas { location = var.gcp_region }
    }
  }
  labels = { label = "gcp" }
}



resource "google_secret_manager_secret_version" "v_projec_id" {
  secret        = google_secret_manager_secret.project_id.id
  secret_data   = var.gcp_project_id
}

resource "google_secret_manager_secret_version" "v_django_secret" {
  secret        = google_secret_manager_secret.django_secret.id
  secret_data   = var.django_secret_key
}

resource "google_secret_manager_secret_version" "v_database_name" {
  secret        = google_secret_manager_secret.database_name.id
  secret_data   = var.db_name
}

resource "google_secret_manager_secret_version" "v_database_user_name" {
  secret        = google_secret_manager_secret.database_user_name.id
  secret_data   = var.db_user_name
}

resource "google_secret_manager_secret_version" "v_database_user_password" {
  secret        = google_secret_manager_secret.database_user_password.id
  secret_data   = var.db_user_password
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

resource "google_secret_manager_secret_version" "v_reserved_ip" {
  secret        = google_secret_manager_secret.reserved_ip.id
  secret_data   = google_compute_global_address.static_ip.address
}



resource "google_secret_manager_secret_iam_binding" "binding_project_id" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.project_id.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}

resource "google_secret_manager_secret_iam_binding" "binding_django_secret" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.django_secret.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}

resource "google_secret_manager_secret_iam_binding" "binding_database_name" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.database_name.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}

resource "google_secret_manager_secret_iam_binding" "binding_database_user_name" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.database_user_name.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}

resource "google_secret_manager_secret_iam_binding" "binding_database_user_password" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.database_user_password.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
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

resource "google_secret_manager_secret_iam_binding" "binding_reserved_ip" {
  project = module.project_services.project_id
  secret_id = google_secret_manager_secret.reserved_ip.secret_id
  role = "roles/secretmanager.secretAccessor"
  members = ["serviceAccount:${google_service_account.custom_service_account.email}"]
}