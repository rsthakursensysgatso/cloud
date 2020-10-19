#!/bin/bash

comm=/bin/netstat
val="-ntpl"
log=/tmp/service_stat
x=0
pstat=/tmp/plog
perf=`vmstat 1 1|awk '{print $4}'|tail -1`

echo " Free Memory $perf" > $pstat
$comm $val |grep httpd

if [ $? -ne 0 ]
then
#echo $perf > $plog
echo "Service httpd is down" > $log
cat $log | mail -s "Service httpd Down" rsthakur83@yahoo.com

while  [ $x -le 4 ];
do
 sleep 4
 echo "Trying httpd service to start " >> $log
 service httpd start
 if [ $? -eq 0 ]
then
 echo " Service httpd has been started after $x attempts." >> $log
 cat $log | mail -s "Service httpd has been started after $x attempts" rsthakur83@yahoo.com
break
else
  echo "Service httpd can't be started after $x attempts." >> $log
 (( x++ ))

fi
done

else
echo "Running fine"
fi
