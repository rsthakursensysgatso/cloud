provider "aws" {
    region = "us-east-1"
}




resource "aws_route" "internet_access1" {
  route_table_id         = "rtb-20026258"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "igw-f993009f"
}


resource "aws_subnet" "public_1c" {
    vpc_id = "vpc-0555f37c"
    cidr_block = "10.0.3.0/24"
    map_public_ip_on_launch = "true"
    availability_zone = "us-east-1b"
    tags {
        Name = "Public 1C"
    }
}

resource "aws_subnet" "public_1d" {
    vpc_id = "vpc-0555f37c"
    cidr_block = "10.0.4.0/24"
    map_public_ip_on_launch = "true"
    availability_zone = "us-east-1c"
    tags {
        Name = "Public 1D"
    }
}




resource "aws_security_group" "allow_ssh1" {
  name = "allow_all_ssh"
  description = "Allow inbound SSH traffic from my IP"
  vpc_id = "vpc-0555f37c"

  ingress {
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

 tags {
    Name = "Allow SSH1"
  }
}

resource "aws_security_group" "web_server1" {
  name = "web server1"
  description = "Allow HTTP and HTTPS traffic in, browser access out."
  vpc_id = "vpc-0555f37c"

  ingress {
      from_port = 80
      to_port = 80
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
      from_port = 0
      to_port = 65535
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
}









resource "aws_key_pair" "deployer" {
 key_name = "myappkeypair3"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDaj8nDzZrLXtfXpg3Uo71wrTfgVPMMLLdPRPPjj8hD1vRoAhkXpdluv4rDYJ6YucRZp7TGcnU2X6DaaEKMUayd7YAN99pf3v9Hm13n/dGc6rJZDTlu9jxaUuJIfSYQv4I7F/ZtixSsqYG1QAIw6KaRWhNO7OvfSMehMn0/4wVTS6fDJuCmo7MlFDU/KidRv3TT5sz+cc+OcYMUuczNtub3BSu+5x1sLLBQtYbntDs1oCAkJJ1yblE74dQMsNduC8fdFsRIJyRGGyQjCPB9gfImBlQu+zGgkgPmi2YEA1/x96v2jo6+L3ZIoFrpkmzuV8dGmmOrpEIEZZtKmi8DxP8L root@lap-am0044476.bccs.hutch.co.id"
}



resource "aws_launch_configuration" "machine-factory-v2" {
    name = "machine-factory-v2"
#    image_id = "ami-2051294a"
    image_id = "ami-b63769a1"
    key_name = "myappkeypair3"
     security_groups = ["${aws_security_group.web_server1.id}","${aws_security_group.allow_ssh1.id}"]
    instance_type = "t2.micro"
    user_data       = "${file("userdata.sh")}"
    lifecycle              { create_before_destroy = true }
}


resource "aws_autoscaling_group" "machine-factory-v2" {
  availability_zones = ["us-east-1b", "us-east-1c"]
  name = "machine-factory-v2"
  min_size = 2
  max_size = 10
  desired_capacity = 2
  health_check_grace_period = 80
  health_check_type = "ELB"
  force_delete = true
  launch_configuration = "${aws_launch_configuration.machine-factory-v2.name}"
  load_balancers = ["web-elb"]
  vpc_zone_identifier = ["${aws_subnet.public_1c.id}","${aws_subnet.public_1d.id}"]
}



output "Autoscaling group" {
  value = "${aws_autoscaling_group.machine-factory-v2.name}"
}

output "subnet 1C id" {
  value = "${aws_subnet.public_1c.id}"
}

output "subnet 1D id" {
 value =  "${aws_subnet.public_1d.id}"
}
