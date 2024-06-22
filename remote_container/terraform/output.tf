
output "redis_ip_address" {
  value = google_redis_instance.memorystore_redis_instance.host
}

output "static_bucket_name" {
  value = google_storage_bucket.static_bucket.name
}

output "media_bucket_name" {
  value = google_storage_bucket.media_bucket.name
}