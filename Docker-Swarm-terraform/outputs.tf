output "master.ip" {
  value = "${aws_instance.master.public_ip}"
}

output "s3_bucket_name" {
 value = "${var.bucket_name}"
}
