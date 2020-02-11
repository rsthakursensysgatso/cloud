variable "ecs_cluster" {
  description = "ECS cluster name"
  default = "fourthline_ecs_cluster"
}

variable "ecs_key_pair_name" {
  description = "EC2 instance key pair name"
  default = "fourthline_keypair"
}


variable "public_key" {
  description = "EC2 instance public key"
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDaj8nDzZrLXtfXpg3Uo71wrTfgVPMMLLdPRPPjj8hD1vRoAhkXpdluv4rDYJ6YucRZp7TGcnU2X6DaaEKMUayd7YAN99pf3v9Hm13n/dGc6rJZDTlu9jxaUuJIfSYQv4I7F/ZtixSsqYG1QAIw6KaRWhNO7OvfSMehMn0/4wVTS6fDJuCmo7MlFDU/KidRv3TT5sz+cc+OcYMUuczNtub3BSu+5x1sLLBQtYbntDs1oCAkJJ1yblE74dQMsNduC8fdFsRIJyRGGyQjCPB9gfImBlQu+zGgkgPmi2YEA1/x96v2jo6+L3ZIoFrpkmzuV8dGmmOrpEIEZZtKmi8DxP8L root@lap-am0044476.bccs.hutch.co.id"
}



variable "region" {
  description = "AWS region"
  default = "us-east-1"
}

variable "availability_zone" {
  description = "availability zone used for the demo, based on region"
  default = ["us-east-1a", "us-east-1b"]
}

########################### Test VPC Config ################################

variable "test_vpc" {
  description = "VPC name for Test environment"
  default = "test_vpc"
}

variable "test_network_cidr" {
  description = "IP addressing for Test Network"
  default = "10.0.0.0/16"
}

variable "test_public_01_cidr" {
  description = "Public 0.0 CIDR for externally accessible subnet"
  default = "10.0.1.0/24"
}

variable "test_public_02_cidr" {
  description = "Public 0.0 CIDR for externally accessible subnet"
  default = "10.0.2.0/24"
}


variable "test_public_03_cidr" {
  description = "Private CIDR"
  default = "10.0.3.0/24"
}

variable "test_public_04_cidr" {
  description = "Private CIDR"
  default = "10.0.4.0/24"
}


variable "ami_id" {
 description = "AMI ID" 
 default = "ami-fad25980"
}
########################### Autoscale Config ################################

variable "max_instance_size" {
  description = "Maximum number of instances in the cluster"
  default = "4"
}

variable "min_instance_size" {
  description = "Minimum number of instances in the cluster"
  default = "2"
}

variable "desired_capacity" {
  description = "Desired number of instances in the cluster"
  default = "2"
}


variable "s3_bucket" {
 description = "S3 Bucket"
  default = "testbucket-fourthline"
}



###################








variable "cluster_name" {
  description = "ecs_cluster"
  default = "ecs_cluster"
}

variable "service_name" {
  description = "testecsservice"
  default = "testecsservice"
}

variable "evaluation_periods" {
  default = "4"
}

variable "period_down" {
  default = "120"
}

variable "period_up" {
  default = "60"
}

variable "threshold_up" {
  default = "75"
}

variable "threshold_down" {
  default = "25"
}

variable "statistic" {
  default = "Average"
}

variable "min_capacity" {
  default = "1"
}

variable "max_capacity" {
  default = "4"
}

variable "lowerbound" {
  default = "0"
}

variable "upperbound" {
  default = "0"
}

variable "scale_up_adjustment" {
  default = "1"
}

variable "scale_down_adjustment" {
  default = "-1"
}

variable "datapoints_to_alarm_up" {
  default = "4"
}

variable "datapoints_to_alarm_down" {
  default = "4"
}
