#Installing dependencies in layer directory for dependency layer
resource "null_resource" "install_layer_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../lambda_layer/requirements.txt -t ${path.module}/../lambda_layer/python/lib/python3.12/site-packages"
  }
  triggers = {
    trigger = timestamp()
  }
}

#Zipping handler function and dependency layer
data "archive_file" "lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir      = "${path.module}/../lambda_extract"
  output_path      = "${path.module}/../extract_lambda.zip"
}

data "archive_file" "layer_dependencies" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../lambda_layer"
  output_path      = "${path.module}/../dependencies.zip"
  depends_on = [
    null_resource.install_layer_dependencies
  ]
}

#Uploading them to the code S3 bucket
resource "aws_s3_object" "file_upload_extract_lambda" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "lambda-functions/extract_lambda.zip"
  source = "${path.module}/../extract_lambda.zip"
}

resource "aws_s3_object" "file_upload_dependencies" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "layers/dependencies.zip"
  source = "${path.module}/../dependencies.zip"
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
  function_name = "extract"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = var.python_runtime
  timeout       = 120
  layers        = [aws_lambda_layer_version.requests_layer_dependencies.arn]
  source_code_hash = data.archive_file.lambda.output_base64sha256
} 

############################### TRANSFORM LAMBDA ##############################

#Zipping handler function
data "archive_file" "transform_lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir      = "${path.module}/../lambda_transform"
  output_path      = "${path.module}/../transform_lambda.zip"
}

#Uploading them to the code S3 bucket
resource "aws_s3_object" "file_upload_transform_lambda" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "lambda-functions/transform_lambda.zip"
  source = "${path.module}/../transform_lambda.zip"
}

#Deploying lambda function
resource "aws_lambda_function" "transform_handler" {
  s3_bucket     = aws_s3_bucket.code.bucket
  s3_key        = "lambda-functions/transform_lambda.zip"
  function_name = "transform"
  role          = aws_iam_role.lambda_role.arn
  handler       = "transform_handler.lambda_handler"
  runtime       = var.python_runtime
  timeout       = 240
  layers = [
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14",
    aws_lambda_layer_version.requests_layer_dependencies.arn
  ]
  source_code_hash = data.archive_file.transform_lambda.output_base64sha256

} 

############################### LOAD LAMBDA ##############################

#Zipping load function
data "archive_file" "load_lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir      = "${path.module}/../lambda_load"
  output_path      = "${path.module}/../load_lambda.zip"
}

#Uploading them to the code S3 bucket
resource "aws_s3_object" "file_upload_load_lambda" {
  bucket = "${aws_s3_bucket.code.id}"
  key    = "lambda-functions/load_lambda.zip"
  source = "${path.module}/../load_lambda.zip"
}

#Deploying lambda function
resource "aws_lambda_function" "load_handler" {
  s3_bucket     = aws_s3_bucket.code.bucket
  s3_key        = "lambda-functions/load_lambda.zip"
  function_name = "load"
  role          = aws_iam_role.lambda_role.arn
  handler       = "load_handler.lambda_handler"
  runtime       = var.python_runtime
  timeout       = 240
  layers = [
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14",
    aws_lambda_layer_version.requests_layer_dependencies.arn
  ]
  source_code_hash = data.archive_file.load_lambda.output_base64sha256

} 
