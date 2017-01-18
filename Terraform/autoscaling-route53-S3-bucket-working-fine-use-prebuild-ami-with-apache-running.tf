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
    availability_zone = "us-east-1b"
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

# instances = ["${aws_instance.web01.id}","${aws_instance.web02.id}"]

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












resource "aws_launch_configuration" "machine-factory-v1" {
    name = "machine-factory-v1"
#    image_id = "ami-2051294a"
    image_id = "ami-f08aa3e7"
#    security_groups = [ "${aws_security_group.allow_web.id}"]
     security_groups = ["${aws_security_group.web_server.id}","${aws_security_group.allow_ssh.id}"]
    instance_type = "t2.micro"
    user_data       = "${file("userdata.sh")}"
    lifecycle              { create_before_destroy = true }
}
 
resource "aws_autoscaling_group" "machine-factory-v1" {
  availability_zones = ["us-east-1b", "us-east-1c"]
  name = "machine-factory-v1"
  min_size = 2
  max_size = 5
  desired_capacity = 3
  health_check_grace_period = 80
#  health_check_type = "EC2"
  health_check_type = "ELB"
  force_delete = false
  launch_configuration = "${aws_launch_configuration.machine-factory-v1.name}"
  load_balancers = ["${aws_elb.web-elb.name}"]
#  vpc_id = "${aws_vpc.myapp.id}"
  vpc_zone_identifier = ["${aws_subnet.public_1a.id}","${aws_subnet.public_1b.id}"]
#  vpc_zone_identifier = ["{$aws_vpc.myapp.id}"]
}






variable "domain" { default = "webappp.io" }
variable "domainAlias" { default = "webappp_io" }
variable "subdomain" { default = "www.webappp.io" }
variable "subdomainAlias" { default = "www_webappp_io" }
variable "cdnSubDomain" { default = "cdn.webappp.io" }


variable "cf_alias_zone_id" {
  description = "Fixed hardcoded constant zone_id that is used for all CloudFront distributions"
  default = "Z2FDTNDATAQYW2"
}

resource "aws_route53_zone" "route53_zone" {
  name = "${var.domain}"
}

resource "aws_route53_record" "website_route53_record" {
  zone_id = "${aws_route53_zone.route53_zone.zone_id}"
  name = "${var.subdomain}"
  type = "A"

  alias {
    name = "${aws_s3_bucket.website_bucket.website_domain}"
    zone_id = "${aws_s3_bucket.website_bucket.hosted_zone_id}"
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "route53_to_cdn" {
  zone_id = "${aws_route53_zone.route53_zone.zone_id}"
  name = "${var.cdnSubDomain}"
  type = "A"

  alias {
    name = "${aws_cloudfront_distribution.cdn.domain_name}"
    zone_id = "${var.cf_alias_zone_id}"
    evaluate_target_health = false
  }
}


resource "aws_s3_bucket" "website_bucket" {

  bucket = "${var.subdomain}"
  acl = "public-read"
  policy = <<POLICY
{
  "Version":"2012-10-17",
  "Statement":[{
    "Sid":"PublicReadForGetBucketObjects",
        "Effect":"Allow",
      "Principal": "*",
      "Action":"s3:GetObject",
      "Resource":["arn:aws:s3:::${var.subdomain}/*"
      ]
    }
  ]
}
POLICY

  website {
    index_document = "index.html"
    error_document = "404.html"
  }
}


resource "aws_cloudfront_distribution" "cdn" {
  depends_on = ["aws_s3_bucket.website_bucket"]
  origin {
    domain_name = "${var.subdomain}.s3.amazonaws.com"
    origin_id = "website_bucket_origin"
    s3_origin_config {
    }
  }
  enabled = true
  default_root_object = "index.html"
  aliases = ["${var.subdomain}"]
  price_class = "PriceClass_200"
  retain_on_delete = true
  default_cache_behavior {
    allowed_methods = [ "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT" ]
    cached_methods = [ "GET", "HEAD" ]
    target_origin_id = "website_bucket_origin"
    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "allow-all"
    min_ttl = 0
    default_ttl = 3600
    max_ttl = 86400
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

