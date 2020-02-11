resource "aws_ecs_service" "fourthline_test_ecs_service" {
  lifecycle {
    create_before_destroy = true
  }
 


  	name            = "testecsservice"
  	iam_role        = aws_iam_role.ecs_service_role.name
  	cluster         = aws_ecs_cluster.test_ecs_cluster.id

  	task_definition = aws_ecs_task_definition.nginx.arn
  	desired_count   = 2

  	load_balancer {
    	target_group_arn  = aws_alb_target_group.ecs_target_group.arn
    	container_port    = 80
    	container_name    = "nginx"
	}
}
