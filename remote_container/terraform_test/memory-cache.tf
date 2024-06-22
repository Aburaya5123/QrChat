# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/redis_instance

resource "google_redis_instance" "memorystore_redis_instance" {
  name           = "${var.project_name}-redis-instance"
  project        = module.project_services.project_id
  tier           = "BASIC"
  memory_size_gb = 2
  region         = var.gcp_region
  redis_version  = "REDIS_6_X"
}