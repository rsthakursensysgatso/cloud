resource "aws_iam_role" "ecs_instance_role" {
    name                = "ecs_instance_role"
    path                = "/"
    assume_role_policy  = data.aws_iam_policy_document.ecs-instance-policy.json
}

data "aws_iam_policy_document" "ecs-instance-policy" {
    statement {
        actions = ["sts:AssumeRole"]

        principals {
            type        = "Service"
            identifiers = ["ec2.amazonaws.com"]
        }
    }
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role-attachment" {
    role       = aws_iam_role.ecs_instance_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs-instance-profile" {
    name = "ecs-instance-profile"
    path = "/"
    role = aws_iam_role.ecs_instance_role.name
    provisioner "local-exec" {
      command = "sleep 10"
    }
}








resource "aws_iam_policy" "fourthline_policy" {
  name        = "fourthline-test-policy"
  description = "A test policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::testbucket-fourthline"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListObject",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::testbucket-fourthline/*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "test_fourthline_attach" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = aws_iam_policy.fourthline_policy.arn
}
