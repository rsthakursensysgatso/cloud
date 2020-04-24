#!/bin/bash
yum -y install httpd wget unzip
systemctl start httpd
chmod 777 -R /var/www/html
cd /var/www/html
echo "<html lang="en"><head>" > index.html
echo "<title>Example page</title>" >> index.html
echo "<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">" >> index.html
echo "</head>" >> index.html
echo "<body>" >> index.html
echo "<p><font size="100" color="blue"><h1>            BLUE       </h1></p>" >> index.html
echo "</body></html>" >> index.html


cd /home/ec2-user
#wget http://ec2-downloads.s3.amazonaws.com/cloudwatch-samples/CloudWatchMonitoringScripts-v1.1.0.zip
#unzip CloudWatchMonitoringScripts-v1.1.0.zip
yum install perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA -y
curl http://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.1.zip -O
unzip CloudWatchMonitoringScripts-1.2.1.zip
chown ec2-user:ec2-user aws-scripts-mon
cd aws-scripts-mon/
#cp awscreds.template awscreds.conf
echo "*/5 * * * * ec2-user /home/ec2-user/aws-scripts-mon/mon-put-instance-data.pl --mem-util --disk-space-util --disk-path=/ --from-cron" >>  /var/spool/cron/ec2-user
