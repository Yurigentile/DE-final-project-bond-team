resource "aws_cloudwatch_event_rule" "scheduler" {
  name        = "run-state-machine-every-20-mins"
  description = "Runs step function on 20 min intervals"
  schedule_expression = "rate(20 minutes)"
}

resource "aws_cloudwatch_event_target" "state_machine_target_resource" {
    rule = aws_cloudwatch_event_rule.scheduler.name
    target_id = "state_machine"
    arn = aws_sfn_state_machine.sfn_state_machine.arn
    role_arn  = aws_iam_role.eventsbridge_invoke_step_functions.arn
}

# resource "aws_lambda_permission" "allow_cloudwatch_to_run_extract_lambda" {
#     statement_id = "AllowExecutionFromCloudWatch"
#     action = "lambda:InvokeFunction"
#     function_name = aws_lambda_function.extract_handler.function_name
#     principal = "states.amazonaws.com"
#     source_arn = aws_sfn_state_machine.sfn_state_machine.arn
# }