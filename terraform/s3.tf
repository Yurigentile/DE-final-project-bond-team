resource "aws_s3_bucket" "data" {
  bucket = var.data_bucket_name
  object_lock_enabled = true
}

resource "aws_s3_bucket" "code" {
  bucket = var.code_bucket_name
}

resource "aws_s3_bucket" "processed" {
  bucket = var.processed_bucket_name
}

# resource "aws_s3_object" "object" {
#   bucket = aws_s3_bucket.data.id
#   key    = "test/test2.txt"
#   source = "test2.txt"
# }
