
#Zipping functions and layers
data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../extract_lambda/handler.py"
  output_path      = "${path.module}/../extract_lambda.zip"
}
data "archive_file" "layer_util_functions" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../src"
  output_path      = "${path.module}/../extract_util_functions.zip"
}
data "archive_file" "layer_dependencies" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../python"
  output_path      = "${path.module}/../dependencies.zip"
}



#Uploading them to the bucket
resource "aws_s3_object" "file_upload_dependencies" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "layers/dependencies.zip"
  source = "${path.module}/../dependencies.zip"
}

resource "aws_s3_object" "file_upload_util_functions" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "layers/utilities.zip"
  source = "${path.module}/../extract_util_functions.zip"
}

resource "aws_s3_object" "file_upload_extract_lambda" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "lambda-functions/extract_lambda.zip"
  source = "${path.module}/../extract_lambda.zip"
}



#Request layers from the bucket
resource "aws_lambda_layer_version" "requests_layer_util_functions" {
  layer_name          = "requests_layer_util_functions"
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_bucket.code.bucket
  s3_key              = aws_s3_object.file_upload_util_functions.key
}

resource "aws_lambda_layer_version" "requests_layer_dependencies" {
  layer_name          = "requests_layer_dependencies"
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_bucket.code.bucket
  s3_key              = aws_s3_object.file_upload_dependencies.key
}


resource "aws_lambda_function" "extract_handler" {
  s3_bucket     = aws_s3_bucket.code.bucket
  s3_key        = "extract_lambda.zip"
  function_name = "Extract"
  role          = aws_iam_role.lambda_role.arn
  handler       = "Extract.handler"
  runtime       = var.python_runtime
  layers        = [aws_lambda_layer_version.requests_layer_dependencies.arn,aws_lambda_layer_version.requests_layer_util_functions.arn]
} 





