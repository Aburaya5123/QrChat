# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions2_function

resource "google_cloudfunctions2_function" "django_task" {
  name        = "django-task"
  location    = var.gcp_region
  description = "django task executor"

  build_config {
    runtime     = "python312"
    entry_point = var.cloud_function_entry_point
    source {
      storage_source {
        bucket = google_storage_bucket.private_bucket.name
        object = google_storage_bucket_object.cloud_function_source_archive.name
      }
    }
  }

  service_config {
    max_instance_count = 10
    min_instance_count = 0
    available_memory   = "256M"
    timeout_seconds    = 30
    environment_variables = {
        BUCKET_NAME = google_storage_bucket.media_bucket.name
    }
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = google_service_account.custom_service_account_cf.email
  }

  event_trigger {
    trigger_region = var.gcp_region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.project_pubsub_topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

data "archive_file" "cloud_function_source" {
  type        = "zip"
  output_path = "django-task.zip"
  source_dir  = var.cloud_function_source
}