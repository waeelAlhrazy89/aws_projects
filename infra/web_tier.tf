resource "aws_s3_bucket" "web" {
  bucket = local.bucket_name
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.web.id
  key          = "index.html"
  content_type = "text/html"
  content      = replace(file("${path.module}/../web_tier/index.html"), "__API_URL__", local.api_url)
}