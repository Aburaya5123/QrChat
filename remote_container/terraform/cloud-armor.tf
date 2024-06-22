
resource "google_compute_security_policy" "policy" {
  name = "custom-policy"

  rule {
    action   = "deny(403)"
    priority = "100"
    match {
        expr {
          expression = "origin.region_code != 'JP' || ! request.path.contains('${var.dns_name}')"
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