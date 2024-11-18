variable "data_bucket_name" {
  type    = string
  default = "nc-project-totes-data"
}

variable "code_bucket_name" {
  type    = string
  default = "nc-project-totes-code"
}

variable "lambda_name" {
  type = string
  default = "extract-handler"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}








