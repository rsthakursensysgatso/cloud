#/bin/bash

kubectl apply -f /home/kube/myapp/nginx.yaml
kubectl apply -f /home/kube/myapp/config-map.yaml
kubectl apply -f /home/kube/myapp/hpa.yaml
kubectl get deployment -n myapp mynginx
if [ $? -eq 0 ]
then

echo "Patching Deployment mynginx"
kubectl patch deployment -n myapp mynginx -p '{"spec":{"template":{"metadata":{"labels":{"build": "'"`date +"%H%M%S"`"'"}}}}}'
else

echo "Deployment mynginx not exist so created above"
fi
