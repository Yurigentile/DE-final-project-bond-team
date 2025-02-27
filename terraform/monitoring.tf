#data source
data "aws_cloudwatch_log_group" "ingestion_lambda_log_group" {
  name = "/aws/lambda/extract"
}

data "aws_cloudwatch_log_group" "transform_lambda_log_group" {
  name = "/aws/lambda/transform"
}

# data "aws_cloudwatch_log_group" "transform_lambda_log_group" {
#   name = "/aws/lambda/load"
# }


#metric filters
resource "aws_cloudwatch_log_metric_filter" "error_metric_filter_ingest" {
  name           = "IngestionLogErrorFilter"
  pattern        = "ERROR"
  log_group_name = data.aws_cloudwatch_log_group.ingestion_lambda_log_group.name
  metric_transformation {
    name      = "IngestionErrorLogCount"
    namespace = "IngestionMetrics"
    value     = "1"
  }
}


resource "aws_cloudwatch_log_metric_filter" "warning_metric_filter_ingest" {
  name           = "IngestionLogWarningFilter"
  pattern        = "WARNING"
  log_group_name = data.aws_cloudwatch_log_group.ingestion_lambda_log_group.name
  metric_transformation {
    name      = "IngestionWarningLogCount"
    namespace = "IngestionMetrics"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "runtimeerror_metric_filter_ingest" {
  name           = "IngestionLogRunTimeErrorFilter"
  pattern        = "RUNTIMEERROR"
  log_group_name = data.aws_cloudwatch_log_group.ingestion_lambda_log_group.name
  metric_transformation {
    name      = "IngestionRunTimeErrorLogCount"
    namespace = "IngestionMetrics"
    value     = "1"
  }
}

#sns topic
resource "aws_sns_topic" "notifications" {
  name = "user-notifications-topic"
}

resource "aws_sns_topic_subscription" "email_notifications_target" {
  topic_arn = aws_sns_topic.notifications.arn
  protocol  = "email"
  endpoint  = "medal.mulish.0w@icloud.com"
}

#metric alarms
resource "aws_cloudwatch_metric_alarm" "error_alert_ingest" {
  alarm_name          = "ingestion-error"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.error_metric_filter_ingest.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.error_metric_filter_ingest.metric_transformation[0].namespace
  period              = 120
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This metric monitors number of errors coming from the Ingestion Lambda in 2 minutes intervals"
  alarm_actions       = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "warning_alert_ingest" {
  alarm_name          = "ingestion-warning"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.warning_metric_filter_ingest.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.warning_metric_filter_ingest.metric_transformation[0].namespace
  period              = 120
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This metric monitors number of warnings coming from the Ingestion Lambda in 2 minutes intervals"
  alarm_actions       = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "runtimeerror_alert_ingest" {
  alarm_name          = "ingestion-runtimeerror"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.runtimeerror_metric_filter_ingest.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.runtimeerror_metric_filter_ingest.metric_transformation[0].namespace
  period              = 120
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This metric monitors number of run time errors coming from the Ingestion Lambda in 2 minutes intervals"
  alarm_actions       = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "transform_errors" {
  alarm_name          = "transform_errors_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  dimensions = {
    FunctionName = aws_lambda_function.transform_handler.function_name
  }
  alarm_actions = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "transform_duration" {
  alarm_name          = "transform_duration_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Average"
  threshold           = "120000"
  dimensions = {
    FunctionName = aws_lambda_function.transform_handler.function_name
  }
  alarm_actions = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "transform_throttles" {
  alarm_name          = "transform_throttles_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  dimensions = {
    FunctionName = aws_lambda_function.transform_handler.function_name
  }
  alarm_actions = [aws_sns_topic.notifications.arn]
}




resource "aws_cloudwatch_metric_alarm" "load_errors" {
  alarm_name          = "load_errors_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  dimensions = {
    FunctionName = aws_lambda_function.load_handler.function_name
  }
  alarm_actions = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "load_duration" {
  alarm_name          = "load_duration_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Average"
  threshold           = "120000"
  dimensions = {
    FunctionName = aws_lambda_function.load_handler.function_name
  }
  alarm_actions = [aws_sns_topic.notifications.arn]
}

resource "aws_cloudwatch_metric_alarm" "load_throttles" {
  alarm_name          = "load_throttles_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  dimensions = {
    FunctionName = aws_lambda_function.load_handler.function_name
  }
  alarm_actions = [aws_sns_topic.notifications.arn]
}