# ---------------
# Lambda IAM Role
# ---------------
# Define

data "aws_iam_policy_document" "trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# Create
resource "aws_iam_role" "lambda_role" {
  name_prefix        = "role-${var.lambda_name}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

# ------------------------------
# Lambda IAM Policy for S3 Write
# ------------------------------
# Define
data "aws_iam_policy_document" "s3_data_policy_doc" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject",

    ]
    resources = ["${aws_s3_bucket.data.arn}/*", "${aws_s3_bucket.data.arn}", "${aws_s3_bucket.processed.arn}/*", "${aws_s3_bucket.processed.arn}"]
  }
}

# Create
resource "aws_iam_policy" "s3_write_policy" {
  name_prefix = "s3-policy-${var.lambda_name}-write"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_s3_write_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}


# ------------------------------
# Lambda IAM Policy for CloudWatch
# ------------------------------

# Define
data "aws_iam_policy_document" "cw_document" {
  statement {
    effect = "Allow"

    actions = [
      "logs:*"
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

# Create
resource "aws_iam_policy" "cw_policy" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.cw_document.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}

# -------------------------------------
# Lambda IAM Policy for secrets manager
# -------------------------------------
# Define
data "aws_iam_policy_document" "secrets_manager_policy_doc" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = ["*"]
  }
}

# Create
resource "aws_iam_policy" "secrets_manager_access_policy" {
  name_prefix = "secrets-manager-policy-${var.lambda_name}-access"
  policy      = data.aws_iam_policy_document.secrets_manager_policy_doc.json
}

# Attach
resource "aws_iam_role_policy_attachment" "secrets_manager_access_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.secrets_manager_access_policy.arn
}

# -------------------------------------
# Lambda IAM Policy for state machine
# -------------------------------------
# Define
resource "aws_iam_role" "iam_for_sfn" {
  name_prefix        = "role-etl-state-machine"
  assume_role_policy = <<EOF
    {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "policy_invoke_lambda" {
  name   = "stepFunctionLambdaFunctionInvocationPolicy"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

# Attach policy to IAM Role for Step Function
resource "aws_iam_role_policy_attachment" "iam_for_sfn_attach_policy_invoke_lambda" {
  role       = aws_iam_role.iam_for_sfn.name
  policy_arn = aws_iam_policy.policy_invoke_lambda.arn
}

# EventBridge IAM
data "aws_iam_policy_document" "events_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "eventsbridge_invoke_step_functions" {
  name               = "eventsbridge-invoke-step-functions"
  assume_role_policy = data.aws_iam_policy_document.events_assume_role.json
}

data "aws_iam_policy_document" "eventsbridge_invoke_step_functions" {
  statement {
    effect    = "Allow"
    actions   = ["states:StartExecution"]
    resources = [aws_sfn_state_machine.sfn_state_machine.arn]
  }
}

resource "aws_iam_policy" "eventbridge_invoke_step_function_policy" {
  name   = "eventbridge_invoke_step_function_policy"
  policy = data.aws_iam_policy_document.eventsbridge_invoke_step_functions.json
}

resource "aws_iam_role_policy_attachment" "attach_eventbridge_policy" {
  role       = aws_iam_role.eventsbridge_invoke_step_functions.name
  policy_arn = aws_iam_policy.eventbridge_invoke_step_function_policy.arn
}
