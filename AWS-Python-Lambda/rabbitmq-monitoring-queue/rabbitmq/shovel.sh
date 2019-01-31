#!/bin/sh



a=$(python3.6 rabbitmq/shovel.py)

curl -i -u lewsupnp:$a -H "content-type:application/json" -XPUT -d'{"value":{"src-uri":"amqp://lewsupnp:reFMl1c1FfD-7D68ISDD6Uxq5GecprYS@duckbill.rmq.cloudamqp.com/lewsupnp","src-queue":"devops-testing-error","dest-uri":"amqp://lewsupnp:reFMl1c1FfD-7D68ISDD6Uxq5GecprYS@duckbill.rmq.cloudamqp.com/lewsupnp","dest-queue":"devops-testing-error-archive"}}' https://duckbill.rmq.cloudamqp.com/api/parameters/shovel/lewsupnp/my-shovel

sleep 5

curl -i -u lewsupnp:$a -H "content-type:application/json" -XDELETE https://duckbill.rmq.cloudamqp.com/api/parameters/shovel/lewsupnp/my-shovel
