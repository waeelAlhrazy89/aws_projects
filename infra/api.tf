resource "aws_apigatewayv2_api" "tasks" {
  name          = local.api_name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "tasks" {
  api_id                 = aws_apigatewayv2_api.tasks.id
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.tasks.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "tasks" {
  for_each  = toset(["GET /tasks", "POST /tasks", "OPTIONS /tasks"])
  api_id    = aws_apigatewayv2_api.tasks.id
  route_key = each.value
  target    = "integrations/${aws_apigatewayv2_integration.tasks.id}"
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id      = aws_apigatewayv2_api.tasks.id
  name        = var.stage_name
  auto_deploy = true
}

resource "aws_lambda_permission" "api" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tasks.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.tasks.execution_arn}/*/*"
}