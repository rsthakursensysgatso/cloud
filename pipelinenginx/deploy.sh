#/bin/bash

kubectl apply -f myapp/nginx.yaml
kubectl get deployment -n myapp mynginx
if [ $? -eq 0 ]
then

echo "Patching Deployment mynginx"
kubectl patch deployment -n myapp mynginx -p '{"spec":{"template":{"metadata":{"labels":{"build": "ravi"}}}}}'
else

echo "Deployment mynginx not exist and creating"
fi
