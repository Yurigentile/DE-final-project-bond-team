variable "data_bucket_name" {
  type    = string
  default = "nc-project-totes-data"
}

variable "code_bucket_name" {
  type    = string
  default = "nc-project-totes-code"
}


variable "process_bucket_name" {
  type    = string
  default = "nc-project-totes-process"
}

variable "lambda_name" {
  type = string
  default = "extract-handler"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}

variable "extract_event" {
  type    = string
  default = "{\"secret\": \"totes-database\",\"bucket\": \"nc-project-totes-data\"}"
}









