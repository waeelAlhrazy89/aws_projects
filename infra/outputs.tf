output "api_url" {
  description = "Address of the tasks API"
  value       = local.api_url
}

output "web_url" {
  description = "Address of the web page"
  value       = "http://localhost:4566/${aws_s3_bucket.web.id}/index.html"
}