# How to configure and deploy FTP service in kubernetes

The purpose of this documentation is to explain  how to setup ftp service in kubernetes cluster for any customer

Below steps need to perform to deploy the ftp service.

- Here we have taken the example of columbia as our client where this ftp service is currently deployed. Because the kubernetes cluster for coloumbia client is hosted On-premises and do not any mechanism to expose ftp service externally (outside kubernetes cluster) so to fulfill this requirement we have used metallb as a load balancer for ftp which can expose ftp service running on port 2169 to external world.

Follow below steps to configure Metallb load balancer on kubernetes cluster. To read more about Metallb go through its documentaion link mentioned here (<https://metallb.universe.tf/>). As a short description it allows to create load balancer on bare metal where cloud provider (such as AWS, GCP or Azure) is not an option.

## Build ftp docker image

Dockerfile which used to build the ftp image exist under the directory docker-vsftpd.

```sh
cd docker-vsftpd

docker build -t us.gcr.io/xilium-1330/coloumbia-vsftpd-server:v1.0.0 .

docker push us.gcr.io/xilium-1330/coloumbia-vsftpd-server:v1.0.0
```

## MetalLB Load Balancer Setup

```sh
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.4/manifests/namespace.yaml

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.4/manifests/metallb.yaml

kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"

apiVersion: v1
kind: ConfigMap
metadata:
    namespace: metallb-system
    name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.10.37-192.168.10.39
```

### Create file named as metallb-config.yaml

Ip address 192.168.10.37 is reserved in the network to be assigned to load balancer for ftp service. Choose this ip address as per your network and update the same in ftp-service.yaml file ```loadBalancerIP: 192.168.10.37```

```sh

apiVersion: v1
kind: ConfigMap
metadata:
    namespace: metallb-system
    name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.10.37-192.168.10.39
```

Here is the list of manifest need to be deployed on kubernetes.

```sh
kubectl apply -f metallb-config.yaml
kubectl apply -f ftp-deployment.yaml
kubectl apply -f ftp-service.yaml
kubectl apply -f task-pv-volume.yaml
kubectl apply -f task-pv-claim.yaml
```

Above command will create ftp deployment, service, physical volumes and claims. Volumeclaims are used to store the ftp user data and ftp users, passwords. Volumes make sure that even ftp pod restart we don't loose user data.

```sh
We can see below ftp service assigned a load balancer and ip address of lb is same ```loadBalancerIP: 192.168.10.37``` as we defined in the ftp-service.yaml.

ftp            LoadBalancer   10.43.233.230   192.168.10.37   2121:31306/TCP,21101:31664/TCP,21102:30339/TCP,21103:32059/TCP,21104:30310/TCP,21105:31358/TCP,21106:30614/TCP,21107:30592/TCP,21108:32745/TCP,21109:30201/TCP,21100:31859/TCP,21111:32245/TCP,21112:30163/TCP,21113:30360/TCP,21114:30010/TCP,21115:32316/TCP,21116:30494/TCP,21117:30729/TCP,21118:32535/TCP,21119:31129/TCP,21120:32051/TCP   4d2h
```

## Steps to add new ftp user

FTP user & password exist in the file /ftpusers/virtual_users.txt on ftp pod under the path /ftpusers/ and to add new user simply update this file with new username and password after that create directory with name similar to username under /home/vsftpd/<'username'>. Because this is pod so we cannot restart ftp server and need to restart the pod to reflect the changes. So simply delete the running ftp pod, deployment will create new pod with new config.

## Note

- Namespace we used here is xilium so change as per your requirement
- This FTP is configured to operate in passive mode so that pre-defined port range (2121, 21101-21120)can be assigned to  remote user connecting to ftp service. Ask IT team to open port 2121 and range 21101-21120 so that remote user can connect. Also configure firewall port forwarding to load balancer ip address 192.168.10.37 at port 2121.
- This doc is referred to build the ftp docker image <https://github.com/fauria/docker-vsftpd>
- To enable SSL update below values in ftp-deployment.yaml

```sh
        - name: SSL_ENABLE
          value: "NO"
        - name: SSL_CERT
          value: "/ftp-ssl-cert/vsftpd.pem"
        - name: SSL_PRIVATE_KEY
          value: "/ftp-ssl-cert/vsftpd.pem"
        - name: SSL_CIPHER
          value: "HIGH"
        - name: SSL_TLSv1
          value: "YES"
        - name: SSL_SSLv2
          value: "NO"
        - name: SSL_SSLv3
          value: "NO"
        - name: FORCE_LOCAL_DATA_SSL
          value: "NO"  
        - name: FORCE_LOCAL_LOGIN_SSL
          value: "NO"

Create base64 format certificate and update ftp-secret.yaml file

base64 -w 0  vsftpd.pem  > ftp.pem          

example:
ftp-secrets.yaml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: ftp-ssl-cert
data:
  vsftpd.pem: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktjd2dnU2pBZ0VBQW9JQkFRRE1WMVlsVEIzcG   FEQlgKbkxjYlN1eW9aUUlIcDN6dFRoNXQ5ZmdNNStWbktidFRmeDBvZCtGSmthMzZZSzFRM0NHd2lLS084MVdQamVNUwp6cGY0VFFQRXM5Tm1EN3FYa2lCR3pzTEhvMlgzWG   FVdklEZ3BERGhVNUZGdjd4YkFsaVNxSUhBSjdiSkF
  
```