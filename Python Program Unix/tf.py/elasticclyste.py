resource "aws_security_group" "redis" {
  vpc_id = "${aws_vpc.myapp.id}"

  tags {
    name = "${var.tag_name}"
    description = "${var.tag_description}"
    environment = "${var.tag_environment}"
    creator = "${var.tag_creator}"
    customer = "${var.tag_customer}"
    owner = "${var.tag_owner}"
    product = "${var.tag_product}"
    costcenter = "${var.tag_costcenter}"
  }
}

#
# ElastiCache resources
#

resource "aws_elasticache_subnet_group" "default" {
  name = "subnet-group-${var.tag_customer}-${var.tag_product}-${var.tag_environment}"
  description = "Private subnets for the ElastiCache instances: ${var.tag_customer} ${var.tag_product} ${var.tag_environment}"
  subnet_ids = ["${aws_subnet.public_1a.id}, {aws_subnet.public_1a.id},{aws_subnet.public_1c.id}, {aws_subnet.public_1d.id}"]
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id = "${var.tag_customer}-${var.tag_product}-${var.tag_environment}"
  engine = "redis"
  engine_version = "2.8.24"
  maintenance_window = "sun:05:00-sun:06:00}"
  node_type = "cache.m3.medium"
  num_cache_nodes = "1"
  parameter_group_name = "default.redis2.8"
  port = "6379"
  subnet_group_name = "${aws_elasticache_subnet_group.default.name}"
  security_group_ids = ["${aws_security_group.redis.id}"]

  tags {
    name = "${var.tag_name}"
    description = "${var.tag_description}"
    environment = "${var.tag_environment}"
    creator = "${var.tag_creator}"
    customer = "${var.tag_customer}"
    owner = "${var.tag_owner}"
    product = "${var.tag_product}"
    costcenter = "${var.tag_costcenter}"
  }
}
