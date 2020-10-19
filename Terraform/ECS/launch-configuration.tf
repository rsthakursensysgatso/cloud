resource "aws_launch_configuration" "ecs_launch_configuration" {
    name                        = "ecs_launch_configuration"
    image_id                    = var.ami_id
    instance_type               = "t2.micro"
    iam_instance_profile        = aws_iam_instance_profile.ecs-instance-profile.id

    root_block_device {
      volume_type = "standard"
      volume_size = 100
      delete_on_termination = true
    }

    lifecycle {
      create_before_destroy = true
    }

    security_groups             = [aws_security_group.test_public_sg.id]
    key_name                    = "fourthline_keypair"
    user_data                   = <<EOF
                                  #!/bin/bash
                                  echo ECS_CLUSTER=ecs_cluster >> /etc/ecs/ecs.config
                                  EOF
}


resource "aws_key_pair" "deployer" {
 key_name = var.ecs_key_pair_name
  public_key = var.public_key
}
