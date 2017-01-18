# Configure the AWS Provider
# Configure the AWS Provider
provider "aws" {
    access_key = ""
    secret_key = ""
    region = "us-east-1"
}




resource "aws_vpc" "myapp" {
     cidr_block = "10.0.0.0/16"
}

resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.myapp.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.gw.id}"
}


resource "aws_subnet" "public_1a" {
    vpc_id = "${aws_vpc.myapp.id}"
    cidr_block = "10.0.1.0/24"
    map_public_ip_on_launch = "true"
    availability_zone = "us-east-1a"
    tags {
        Name = "Public 1A"
    }
}

resource "aws_subnet" "public_1b" {
    vpc_id = "${aws_vpc.myapp.id}"
    cidr_block = "10.0.2.0/24"
    map_public_ip_on_launch = "true"
    availability_zone = "us-east-1c"
    tags {
        Name = "Public 1B"
    }
}


resource "aws_internet_gateway" "gw" {
    vpc_id = "${aws_vpc.myapp.id}"

    tags {
        Name = "myapp gw"
    }
}



resource "aws_security_group" "allow_ssh" {
  name = "allow_all"
  description = "Allow inbound SSH traffic from my IP"
  vpc_id = "${aws_vpc.myapp.id}"

  ingress {
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

 tags {
    Name = "Allow SSH"
  }
}

resource "aws_security_group" "web_server" {
  name = "web server"
  description = "Allow HTTP and HTTPS traffic in, browser access out."
  vpc_id = "${aws_vpc.myapp.id}"

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




resource "aws_instance" "web01" {
    ami = "ami-2051294a"
    instance_type = "t2.micro"
    subnet_id = "${aws_subnet.public_1a.id}"
    security_groups = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]
    key_name = "myappkeypair"
    vpc_security_group_ids = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]
     provisioner "file" {
       source = "/tmp/script.sh"
       destination = "/tmp/script.sh"

 connection {
    user = "ec2-user"
    key_file = "/root/.ssh/id_rsa"
    agent = false
}

    }
    provisioner "remote-exec" {
      inline = [
        "chmod +x /tmp/script.sh",
         "/tmp/script.sh args"
        ]
    connection {
    user = "ec2-user"
    key_file = "/root/.ssh/id_rsa"
    agent = false
  }


  }

       provisioner "file" {
       source = "/var/log/html1/index.html"
       destination = "/var/www/html/index.html"

 connection {
    user = "ec2-user"
    key_file = "/root/.ssh/id_rsa"
    agent = false
}
    }




tags {
        Name = "web01"
    }
}


resource "aws_instance" "web02" {
    ami = "ami-2051294a"
    instance_type = "t2.micro"
    subnet_id = "${aws_subnet.public_1b.id}"
    security_groups = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]
    key_name = "myappkeypair"
    vpc_security_group_ids = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]
       provisioner "file" {
       source = "/tmp/script.sh"
       destination = "/tmp/script.sh"

 connection {
    user = "ec2-user"
    key_file = "/root/.ssh/id_rsa"
    agent = false
}
    }

    provisioner "remote-exec" {
      inline = [
        "chmod +x /tmp/script.sh",
         "/tmp/script.sh args"
        ]

    connection {
    user = "ec2-user"
    key_file = "/root/.ssh/id_rsa"
    agent = false
  }


  }

       provisioner "file" {
       source = "/var/log/html2/index.html"
       destination = "/var/www/html/index.html"

 connection {
    user = "ec2-user"
    key_file = "/root/.ssh/id_rsa"
    agent = false
}
    }


  

tags {
        Name = "web02"
    }
}



resource "aws_elb" "web-elb" {
  name = "web-elb"
  subnets  = ["${aws_subnet.public_1a.id}","${aws_subnet.public_1b.id}"]
  security_groups = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]

  listener {
    instance_port = 80
    instance_protocol = "http"
    lb_port = 80
    lb_protocol = "http"
  }

 health_check {
    healthy_threshold = 2
    unhealthy_threshold = 2
    timeout = 3
    target = "HTTP:80/"
    interval = 30
  }

 instances = ["${aws_instance.web01.id}","${aws_instance.web02.id}"]

  cross_zone_load_balancing = true
  idle_timeout = 400
  connection_draining = true
  connection_draining_timeout = 400

  tags {
    Name = "Web ELB"
  }

}

resource "aws_key_pair" "deployer" {
 key_name = "myappkeypair"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDaj8nDzZrLXtfXpg3Uo71wrTfgVPMMLLdPRPPjj8hD1vRoAhkXpdluv4rDYJ6YucRZp7TGcnU2X6DaaEKMUayd7YAN99pf3v9Hm13n/dGc6rJZDTlu9jxaUuJIfSYQv4I7F/ZtixSsqYG1QAIw6KaRWhNO7OvfSMehMn0/4wVTS6fDJuCmo7MlFDU/KidRv3TT5sz+cc+OcYMUuczNtub3BSu+5x1sLLBQtYbntDs1oCAkJJ1yblE74dQMsNduC8fdFsRIJyRGGyQjCPB9gfImBlQu+zGgkgPmi2YEA1/x96v2jo6+L3ZIoFrpkmzuV8dGmmOrpEIEZZtKmi8DxP8L root@lap-am0044476.bccs.hutch.co.id"
}












#resource "aws_launch_configuration" "machine-factory-v1" {
#    name = "machine-factory-v1"
#    image_id = "ami-2051294a"
#     security_groups = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]
#    instance_type = "t2.micro"
#}
 
#resource "aws_autoscaling_group" "machine-factory-v1" {
#  availability_zones = ["us-east-1a", "us-east-1c"]
#  name = "machine-factory-v1"
#  min_size = 2
#  max_size = 2
#  desired_capacity = 2
#  health_check_grace_period = 60
#  health_check_type = "EC2"
#  force_delete = false
#  launch_configuration = "${aws_launch_configuration.machine-factory-v1.name}"
#  load_balancers = ["${aws_elb.web-elb.name}"]
#  vpc_zone_identifier = ["${aws_subnet.public_1a.id}","${aws_subnet.public_1b.id}"]
#}
