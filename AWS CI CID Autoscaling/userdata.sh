#!/bin/bash
yum -y install httpd wget git
systemctl start httpd
chmod 777 -R /var/www/html
git  init 
