data "aws_ecs_task_definition" "nginx" {
  task_definition = aws_ecs_task_definition.nginx.family
}

resource "aws_ecs_task_definition" "nginx" {


    family                = "nginx"
    container_definitions = <<DEFINITION
[
  {
    "name": "nginx",
    "image": "nginx",
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 8080
      }
    ],
    "memory": 500,
    "cpu": 10
  }
]
DEFINITION
}
