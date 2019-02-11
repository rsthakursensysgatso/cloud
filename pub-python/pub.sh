#!/bin/bash

# connect to cloudAMQP

host='duckbill.rmq.cloudamqp.com'
port='443'
user='lewsupnp'
pass='reFMl1c1FfD-7D68ISDD6Uxq5GecprYS'

#if [[ "$#" -eq 0 ]]; then
#        echo "$0 {some rabbit command, eg list queues} "
#        echo "    try $0 help, or $0 help subcommands."
#        exit 1
#fi

rabbitmqadmin --host=$host --port=$port --ssl --vhost=$user --username=$user --password=$pass publish exchange=devops-testing-error routing_key=devops-testing-error payload="Helooooo World!!!!!!"
#rabbitmqadmin --host=$host --port=$port --ssl --vhost=$user --username=$user --password=$pass list queues


