locals {
  table_name    = "${title(var.project)}${upper(var.suffix)}"
  role_name     = "${var.project}-lambda-role-${var.suffix}"
  function_name = "${var.project}-api-${var.suffix}"
  api_name      = "${var.project}-http-api-${var.suffix}"
  bucket_name   = "${var.project}-web-${var.suffix}"

  api_url = "http://${aws_apigatewayv2_api.tasks.id}.execute-api.localhost.floci.io:4566/${var.stage_name}/tasks"

  tags = {
    project = "three-tier"
  }
}