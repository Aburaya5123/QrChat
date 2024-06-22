
resource "google_pubsub_topic" "project_pubsub_topic" {
  name    = "main-topic"
  project = module.project_services.project_id
}