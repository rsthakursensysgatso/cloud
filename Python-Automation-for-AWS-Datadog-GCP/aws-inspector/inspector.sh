#!/bin/bash

filter=`cat /tmp/findings| cut -d '"' -f2 > /tmp/output`
sed '1d;$d' "/tmp/output" > /tmp/finallist

for i in `cat /tmp/finallist`
do

val=`aws inspector describe-findings  --finding-arns $i`
python3.6 conversion.py "$val"
done

### for date range
# aws inspector list-findings --filter "creationTimeRange={beginDate='2019-03-01',endDate='2019-04-01'}"
##
