#!/bin/bash

sub1=`aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-2c70d755|grep SubnetId|awk '{print $2}'|cut -c 2-16|head -1`
sub2=`aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-2c70d755|grep SubnetId|awk '{print $2}'|cut -c 2-16|tail -1`
echo "Subnet 1 $sub1"
echo "Subnet 2 $sub2"
envr="`aws autoscaling describe-auto-scaling-groups|grep LaunchConfigurationName|head -1|awk '{print $2}'|cut -c 2-19`"
lcfg1="machine-factory-v1"
lcfg2="machine-factory-v2"
echo $envr
if [ "$envr" == "$lcfg1" ]
then
  echo $envr
  echo "Swaping environment blue with green"
else
  echo "Swaping environment blue with green"
  
fi
