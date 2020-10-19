resource "aws_s3_bucket" "testbucket_fourthline" {
  bucket = var.s3_bucket
  acl    = "private"

  tags = {
    Name        = "Fourthline bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_public_access_block" "fourthline_example" {
  bucket = aws_s3_bucket.testbucket_fourthline.id
  block_public_acls   = true
  block_public_policy = true
}
