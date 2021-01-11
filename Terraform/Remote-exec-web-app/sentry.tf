provider "aws" {
    region = var.reg
}

resource "aws_security_group" "allow_ssh" {
  name = "allow_all"
  description = "Allow inbound SSH traffic from my IP"
  vpc_id = var.vpcid

  ingress {
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

 tags = {
    Name = "Allow SSH"
  }
}

resource "aws_security_group" "web_server" {
  name = "web server"
  description = "Allow HTTP and HTTPS traffic in, browser access out."
  vpc_id = var.vpcid

  ingress {
      from_port = 443
      to_port = 443
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
      from_port = 0
      to_port = 65535
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

 tags = {
    Name = "Allow HTTPS"
  }

}


resource "aws_instance" "sentry-arachnys-task" {
    ami = var.ami_id
    instance_type = var.instance_t
    subnet_id = var.subnetid
    security_groups = [aws_security_group.web_server.id,aws_security_group.allow_ssh.id]
    key_name = var.keyname
    vpc_security_group_ids = [aws_security_group.web_server.id,aws_security_group.allow_ssh.id]
    tags = {
      Name = "sentry-arachnys-task"
    }
}


resource  "null_resource" "copy_execute" {

 connection {
    type = "ssh"
    user = "ubuntu"
    private_key  = file(var.pvt_key)
    host     = aws_instance.sentry-arachnys-task.public_ip
    timeout = "3m"
    agent = false
}


 provisioner "file" {
 source = "./files"
 destination = "/tmp/"

}


 provisioner "remote-exec" {
 inline = [
    "chmod +x /tmp/files/sentry_install.sh",
    "/tmp/files/sentry_install.sh"
      ]
  }

 depends_on = [aws_instance.sentry-arachnys-task]

}


resource "aws_key_pair" "deployer" {
 key_name = var.keyname
  public_key = var.keypair
}


output "app-public-ip" {
  value = aws_instance.sentry-arachnys-task.public_ip
}
