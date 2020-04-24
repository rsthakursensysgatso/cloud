#/bin/bash

kubectl apply -f /home/kube/myapp/flaskapp.yaml
kubectl apply -f /home/kube/myapp/hpa.yaml
kubectl get deployment -n myapp myflaskapp
if [ $? -eq 0 ]
then

echo "Patching Deployment myflaskapp"
kubectl patch deployment -n myapp myflaskapp -p '{"spec":{"template":{"metadata":{"labels":{"build": "'"`date +"%H%M%S"`"'"}}}}}'
else

echo "Deployment myflaskapp not exist so created above"
fi
