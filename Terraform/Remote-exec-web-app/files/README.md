# This documentation include the steps required to install the sentry web app on aws ec2 instance using terraform

## Note: I have used the terraform version v0.12.0 to deploy the aws instance, other resources on aws

Step 1) Update the variable.tf with the value such as region, vpcid, subnet id in vpc, ami_id etc as per the environment and your requirement. I have used the variable 'pvt_key' located (in the linux machine /root/.ssh/id_rsa ) and 'keypair' taken from /root/.ssh/id_rsa.pub and update it in variable.tf

Step 2) gen-cer.sh is the script used to create the self signed certificate which is valid for 1 year and nginx acting as reverse proxy, frontend for sentry app running on port 9000. Nginx is listening on port 443 and will send request to sentry.

Step 3) sentry.arachnys-task.conf is the nginx configuration file

Step 4) sentry_install.sh is the installation script to install the all required packages such as docker, nginx,docker-compose.

Step 5) After above changes in variable.tf run terraform init

Step 6) Run terraform plan to see the resource terraform will create

Step 7) Then run terraform apply and choose option yes to create resources on aws. Here, I have used remote-exec provisioner to push the files, directories onto the instance and for execution of script (sentry_install.sh) script.

Step 8) Terraform creates the security group to allow remote connection at port 443, 22.

Step 9) Once the terraform apply finishes it will show in output the public ip address (app-public-ip) of instance which we can use to update the /etc/hosts for domain for example sentry.arachnys-task.com and now we access sentry app via <https://sentry.arachnys-task.com>
