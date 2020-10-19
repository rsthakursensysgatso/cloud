provider "aws" {
    region = "us-east-1"
}


resource "aws_launch_configuration" "machine-factory-v1" {
    name = "machine-factory-v1"
    image_id = "ami-b63769a1"
    security_groups = ["sg-4557c234","sg-3c55c04d"]
    instance_type = "t2.micro"
    key_name = "myappkeypair"
    user_data       = "${file("userdata.sh")}"
    lifecycle              { create_before_destroy = true }
}


resource "aws_autoscaling_group" "machine-factory-v1" {
  availability_zones = ["us-east-1b", "us-east-1c"]
  name = "machine-factory-v1"
  min_size = 2
  max_size = 10
  desired_capacity = 2
  health_check_grace_period = 80
  health_check_type = "ELB"
  force_delete = false
  launch_configuration = "${aws_launch_configuration.machine-factory-v1.name}"
  load_balancers = ["web-elb"]
  vpc_zone_identifier = ["subnet-1b0d8c37","subnet-f4f188bc"]
}


output "Autoscaling group" {
  value = "${aws_autoscaling_group.machine-factory-v1.name}"
}
