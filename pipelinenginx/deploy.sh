#/bin/bash

kubectl apply -f myapp/nginx.yaml
kubectl patch deployment mynginx -p '{"spec":{"template":{"metadata":{"labels":{"build": "ravi"}}}}}'
