
resource "google_compute_security_policy" "policy" {
  project = module.project_services.project_id
  name = "custom-policy"

  rule {
    action   = "deny(403)"
    priority = "1500"
    match {
        expr {
          expression = "!request.headers['Host'].matches('.*${var.dns_name}.*') && !request.headers[':authority'].matches('.*${var.dns_name}.*')"
        }
    }
  }

  rule {
    action   = "deny(403)"
    priority = "1501"
    match {
        expr {
          expression = "!'[JP,ZZ]'.contains(origin.region_code)"
        }
    }
  }

  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
  }
}