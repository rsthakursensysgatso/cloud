#!/bin/bash



health_check()
{
inst_id=`curl -s http://169.254.169.254/latest/meta-data/instance-id`
ip_add=`curl -s http://169.254.169.254/latest/meta-data/local-ipv4`
avail_zone=`curl http://169.254.169.254/latest/meta-data/placement/availability-zone`
account_id=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | grep -Eo '([[:digit:]]{12})'`
hostname=`curl http://169.254.169.254/latest/meta-data/local-hostname`
#tags=`/home/ubuntu/.local/lib/aws/bin/aws ec2 describe-instances --instance-ids $inst_id --region eu-west-1 --query 'Reservations[*].Instances[*].Tags[?                                      Key]' --output text |grep -vE "cloudformation|autoscaling"`
tags=`/home/ubuntu/.local/lib/aws/bin/aws ec2 describe-instances --instance-ids $inst_id --region eu-west-1 --query 'Reservations[*].Instances[*].Tags[?Key]' --output text |grep -vE "cloudformation|autoscaling"`

Array=($( df -H | grep -vE '^Filesystem|tmpfs|cdrom|loop' | awk '{ print $6 }'))

for i in "${Array[@]}"
do
diskspace=`df -h $i|tail -1|awk '{print $5}'|sed 's/%//g'`
echo $diskspace
if [ $diskspace -gt  80 ] && [ $diskspace -lt 90 ]
then

curl -X POST -H 'Content-type: application/json' --data '{"text":"'"(Warning Alert!! $i mount point usage is above $diskspace% on Instance ID: $inst_id                                         Hostname: $hostname   Private-IP:$ip_add   AccountID: $account_id  Region: $avail_zone \n Tags: $tags)"'"}' https://hooks.slack.com/services/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

elif [ $diskspace -gt  90 ]
then

curl -X POST -H 'Content-type: application/json' --data '{"text":"'"(Critical Alert!! $i mount point usage is above $diskspace% on Instance ID: $inst_id                                         Hostname: $hostname   Private-IP:$ip_add   AccountID: $account_id  Region: $avail_zone   Tags: $tags)"'"}' https://hooks.slack.com/services/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

echo $tags
echo $inst_id
echo $ip_add
echo $avail_zone
echo $account_id

fi
done
}


ls -ld /home/ubuntu/.local/lib/aws/bin/aws
if [ $? -eq 0 ];then
health_check
else

sudo apt-get install unzip python -y
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip  awscli-bundle.zip
./awscli-bundle/install  /home/ubuntu/awscli
health_check

fi
