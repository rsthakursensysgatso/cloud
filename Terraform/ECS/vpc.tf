resource "aws_vpc" "test_vpc" {
  cidr_block = var.test_network_cidr
}



resource "aws_subnet" "test_public_sn1" {
  vpc_id     = aws_vpc.test_vpc.id
  cidr_block = var.test_public_01_cidr
  availability_zone = var.availability_zone[0]

}

resource "aws_subnet" "test_public_sn2" {
  vpc_id     = aws_vpc.test_vpc.id
  cidr_block = var.test_public_02_cidr
  availability_zone = var.availability_zone[1]

}


resource "aws_security_group" "test_public_sg" {
  vpc_id = aws_vpc.test_vpc.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

 
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.test_vpc.id
    tags = {
        Name = "fourthline igw"
    }
}


resource "aws_route" "internet_access" {
  route_table_id         = aws_vpc.test_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}




##################

resource "aws_route_table" "my_vpc_test_public_sn" {
    vpc_id = aws_vpc.test_vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    }

    tags = {
        Name = "Public Subnet Route Table"
    }
}

resource "aws_route_table_association" "my_vpc_test_public_sn_01" {
    subnet_id = aws_subnet.test_public_sn1.id
    route_table_id = aws_route_table.my_vpc_test_public_sn.id
}

resource "aws_route_table_association" "my_vpc_test_public_sn_02" {
    subnet_id = aws_subnet.test_public_sn2.id
    route_table_id = aws_route_table.my_vpc_test_public_sn.id
}






resource "aws_subnet" "test_public_sn3" {
  vpc_id     = aws_vpc.test_vpc.id
  cidr_block = var.test_public_03_cidr
  availability_zone = var.availability_zone[0]

}

resource "aws_subnet" "test_public_sn4" {
  vpc_id     = aws_vpc.test_vpc.id
  cidr_block = var.test_public_04_cidr
  availability_zone = var.availability_zone[1]

}



resource "aws_eip" "nat_gw_eip" {
  vpc = true
}

resource "aws_nat_gateway" "gw" {
  allocation_id = aws_eip.nat_gw_eip.id
  subnet_id     =  aws_subnet.test_public_sn1.id
}



resource "aws_route_table" "my_vpc_us_east_1a_nated" {
    vpc_id = aws_vpc.test_vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_nat_gateway.gw.id
    }

    tags = {
        Name = "Main Route Table for NAT-ed subnet"
    }
}

resource "aws_route_table_association" "my_vpc_us_east_1a_nated" {
    subnet_id = aws_subnet.test_public_sn3.id
    route_table_id = aws_route_table.my_vpc_us_east_1a_nated.id
}

resource "aws_route_table_association" "my_vpc_us_east_2a_nated" {
    subnet_id = aws_subnet.test_public_sn4.id
    route_table_id = aws_route_table.my_vpc_us_east_1a_nated.id
}
