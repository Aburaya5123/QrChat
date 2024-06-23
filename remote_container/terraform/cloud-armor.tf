
resource "google_compute_security_policy" "policy" {
  name = "custom-policy"

  rule {
    action   = "deny(403)"
    priority = "100"
    match {
        expr {
          expression = "!request.headers['Host'].matches('.*${var.dns_name}.*') && !request.headers[':authority'].matches('.*${var.dns_name}.com.*')"
        }
    }
  }

  rule {
    action   = "deny(403)"
    priority = "101"
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