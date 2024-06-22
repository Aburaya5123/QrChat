
resource "google_compute_global_address" "static_ip" {
  name    = "${var.project_name}-static-ip"
  project = module.project_services.project_id
}