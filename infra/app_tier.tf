resource "aws_iam_role" "lambda" {
  name = local.role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_db" {
  name = "${var.project}-db-access"
  role = aws_iam_role.lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["dynamodb:Scan", "dynamodb:PutItem", "dynamodb:GetItem"]
      Resource = aws_dynamodb_table.tasks.arn
    }]
  })
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/../app_tier/lambda_function.py"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "tasks" {
  function_name    = local.function_name
  role             = aws_iam_role.lambda.arn
  runtime          = "python3.12"
  handler          = "lambda_function.lambda_handler"
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      TABLE_NAME  = aws_dynamodb_table.tasks.name
      DB_ENDPOINT = var.lambda_endpoint
    }
  }
}