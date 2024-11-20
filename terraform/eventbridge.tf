resource "aws_cloudwatch_event_rule" "scheduler" {
  name        = "run-extract-lambda-every-15-mins"
  description = "Runs quotes.py lambda on 15 min intervals"
  schedule_expression = "rate(15 minutes)"
}

resource "aws_cloudwatch_event_target" "extract_lambda_target_resource" {
    rule = aws_cloudwatch_event_rule.scheduler.name
    target_id = "extract_lambda"
    arn = aws_lambda_function.extract_handler.arn
    input = var.extract_event
}

resource "aws_lambda_permission" "allow_cloudwatch_to_run_extract_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.extract_handler.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.scheduler.arn
}