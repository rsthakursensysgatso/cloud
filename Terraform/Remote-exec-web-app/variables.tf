variable "reg" {
  default = "us-east-1"
}

variable "vpcid" {
  default = "vpc-ecc86d91"
}

variable "pvt_key" {
 default = "/root/.ssh/id_rsa"
}

variable "keypair" {
 default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDH8I2Qz9Enre17bCiOtIerI6kO0e3mGUM5PowL07iHoLDAqLJv6gOBHfSbiJlCQbFjakOmBKXn/Iq7tRn/aHGnZ7fuk9hb2S1A6Wfd9ZhwRz7c4+O6oRqTdi1vgRJThDTXxynlaLteK3TM6H5gSzhzxu+mDpGOkMbbc/zbV7G4xd5qLbqbZyFeLkbOSGJlNXxe+I9HlZQz/lI9OuRguN3doCCGiHApwuW+yVDEXpQDObVeOBF57sdaPCvBfopX+5b+V3Cqye20guzI1ULTeBwQas/LlnQDwDSRVIBQnuehLzkEBbdd24xmR1FgdUnNYD37081M+Y3pj5XuGu/tFWaWp6et9l43018/aGQHoNkBtP0GPYHlanOtcbrJJvo9QWBJWfbE+J/zhk+TM+D0qqsrvPnlDCzTNekvZdjaUFcTAGWWdWU5mnueItl/H02PxYIIfp+WU263XTjh6hojXByC9bHYhRIFc0NBqFQkRMrK9Wgq70fITccOCma69eYEYVU= root@HRLL069"
}

variable "ami_id" {
 default = "ami-0885b1f6bd170450c"
}

variable "instance_t" {
 default = "t2.medium"
}

variable "subnetid" {
 default = "subnet-23aa2345"
}

variable "keyname" {
 default = "myappkeypair"
}
