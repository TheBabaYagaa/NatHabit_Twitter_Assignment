provider "aws" {
  region = "eu-north-1"
}

resource "aws_sqs_queue" "follow_event_queue" {
  name = "follow_event_queue"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_sqs_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_sqs_policy" {
  name = "lambda_sqs_policy"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        Resource = aws_sqs_queue.follow_event_queue.arn
      },
      {
        Effect = "Allow",
        Action = "ses:*",
        Resource = "*"
      }
    ]
  })
}

resource "aws_lambda_function" "follow_event_lambda" {
  function_name = "follow_event_lambda"
  runtime       = "python3.12"
  handler       = "lambda_function.handler"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 10

  filename         = "${path.module}/function.zip"
  source_code_hash = filebase64sha256("${path.module}/function.zip")

  environment {
    variables = {
      SENDER_MAIL = var.SENDER_MAIL
      DEFAULT_RECIPIENT = var.DEFAULT_RECIPIENT
      EMAIL_TEMPLATE = var.EMAIL_TEMPLATE
    }
  }

}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.follow_event_queue.arn
  function_name    = aws_lambda_function.follow_event_lambda.arn
  batch_size       = 5
}
