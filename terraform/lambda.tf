
#Zipping handler function and dependency layer
data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir      = "${path.module}/../extract_lambda"
  output_path      = "${path.module}/../extract_lambda.zip"
}

data "archive_file" "layer_dependencies" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../python"
  output_path      = "${path.module}/../dependencies.zip"
}

#Uploading them to the code S3 bucket
resource "aws_s3_object" "file_upload_extract_lambda" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "lambda-functions/extract_lambda.zip"
  source = "${path.module}/../extract_lambda.zip"
  # source_hash   = filemd5("${path.module}/../extract_lambda.zip")
}

resource "aws_s3_object" "file_upload_dependencies" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "layers/dependencies.zip"
  source = "${path.module}/../dependencies.zip"
  # source_hash   = filemd5("${path.module}/../dependencies.zip")
}

#Deploying layer
resource "aws_lambda_layer_version" "requests_layer_dependencies" {
  layer_name          = "requests_layer_dependencies"
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_bucket.code.bucket
  s3_key              = aws_s3_object.file_upload_dependencies.key
}

#Deploying lambda function
resource "aws_lambda_function" "extract_handler" {
  s3_bucket     = aws_s3_bucket.code.bucket
  s3_key        = "lambda-functions/extract_lambda.zip"
  function_name = "handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = var.python_runtime
  layers        = [aws_lambda_layer_version.requests_layer_dependencies.arn]
  source_code_hash = data.archive_file.lambda.output_base64sha256
} 





