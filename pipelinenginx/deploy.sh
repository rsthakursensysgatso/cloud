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

mypod=`kubectl get pods -n myapp|grep myng|tail -1|awk '{print $1}'`

kubectl port-forward $mypod 31894:80 -n myapp &
