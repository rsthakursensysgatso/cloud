resource "aws_alb" "ecs_load_balancer" {
    name                = "ecsloadbalancer"
    security_groups     = [aws_security_group.test_public_sg.id]
    subnets             = [aws_subnet.test_public_sn1.id, aws_subnet.test_public_sn2.id]

}

resource "aws_alb_target_group" "ecs_target_group" {
    name                = "ecstargetgroup"
    port                = "80"
    protocol            = "HTTP"
    vpc_id              = aws_vpc.test_vpc.id

    health_check {
        healthy_threshold   = "5"
        unhealthy_threshold = "2"
        interval            = "30"
        matcher             = "200"
        path                = "/"
        port                = "8080"
        protocol            = "HTTP"
        timeout             = "5"
    }

  lifecycle {
    create_before_destroy = true
  }

depends_on = [aws_alb.ecs_load_balancer]

    tags = {
      Name = "ecs-target-group"
    }
}

resource "aws_alb_listener" "alb-listener" {
    load_balancer_arn = aws_alb.ecs_load_balancer.arn
    port              = "80"
    protocol          = "HTTP"

    default_action {
        target_group_arn = aws_alb_target_group.ecs_target_group.arn
        type             = "forward"
    }
}
