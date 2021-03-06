# Steps required to setup On-Premise Infra for Puls, Xilium

  1) [Database Installation](#database-installation)
  2) [K3S cluster installation on On-Premise Nodes](#k3scluster)
  3) [Loki, InfluxDB, Grafana & Mail server installation](#logging-&-Monitoring)
  4) [Telegraf, Promtail Installation on K8S](#Telegraf-Promtail-Installation-on-K8s)
  5) [Database logging, monitoring](#database-monitoring)
  6) [RabbitMQ installation and monitoring](#rabbitmq-installation-and-monitoring)

To demonstrate the steps involved in setting up infra here I am taking the example of TRNC customer.

**We have similar setup for colombia client.**

TRNC IT support team provided us 6 VM's named as (k8scl1, k8scl2, k8scl3, k8scl4) are four kubernetes nodes and remainig two are database servers (master dbsrv1 and replica dbsrv2).

## Database Installation

Before we begin with the installation of kubernetes cluster first we need to install postgres database (version 12) on master DB (dbsrv1) and on replica node (dbsrv2). After that create the database k3s which will be used to store k8s cluster state.

Here taking the example of operating system Ubuntu 20.04

```sh
apt -y install postgresql-12

Make following changes in the /etc/postgresql/12/main/postgresql.conf

listen_addresses = '*'
log_min_duration_statement = 1000
logging_collector = on
log_line_prefix= '%m [%p] %d %a %u %h %c '
log_file_mode = 0644
wal_level = replica
max_wal_size = 1GB
min_wal_size = 80MB
max_wal_senders = 10


sudo -u postgres psql
CREATE Database k3s
create user k3s
ALTER ROLE k3s WITH PASSWORD 'xxxxx';
```

Add the following lines in the file /etc/postgresql/12/main/pg_hba.conf to allow network connectivity from the kubernetes pods network and replica DB server dbsrv2. These ip ranges can be different depend on kubernetes pods, svc, network and need changes accordingly.

To check the ip ranges run ```kubectl get svc```, ```kubectl get nodes -o wide```

```sh
host    all             all             127.0.0.1/32            md5
host    all             all             10.98.100.51/32         md5
host    all             all             10.98.100.52/32         md5
host    all             all             10.98.0.0/16            md5
host    all             all             10.43.0.0/16            md5
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
host    replication     replicator      10.98.100.62/32         md5
```

Update the hosts file on each node k8scl1, k8scl2, k8scl3, k8scl4, dbsrv1 & dbsrv2.

```sh
10.98.100.51 k8scl1
10.98.100.52 k8scl2
10.98.100.53 k8scl3
10.98.100.54 k8scl4
10.98.100.61 dbsrv1
10.98.100.62 dbsrv2
```

After the master DB installation finished, setup the replication with the other DB server (dbsrv2) and here is the website link which can be used to configured the replication <https://www.server-world.info/en/note?os=Ubuntu_20.04&p=postgresql12&f=3>

## k3scluster

After database installation and configuration finished we can proceed with the kubernetes installation.

**Note:** Test the connection from the kubernetes nodes to DB server at port 5432 example telnet db ip address at port 5432

To configure master node run below command on both master nodes (k8scl1, k8scl2).

```sh
curl -sfL <https://get.k3s.io> | sh -s - server --datastore-endpoint="postgres://k3s:k3suserpassword@10.98.100.61:5432/k3s"
```

The above command will install the k3s server agent and now it's time to do worker node installation.

Get the token from master node `cat /var/lib/rancher/k3s/server/node-token`, use this token for k3s agent installation on worker node.

Run below command on worker node (k8scl3 & k8scl4)

```sh
curl -sfL https://get.k3s.io | K3S_URL=https://k8scl1:6443 K3S_TOKEN="token-from-master-node" sh -
```

Now we have k8s master and worker node up & running. To test the cluster current state run ```kubectl get nodes``` command on any one of the master node.

```sh
root@k8scl1:~# kubectl get nodes
NAME         STATUS   ROLES                  AGE   VERSION
k8scl1   Ready    control-plane,master   12d   v1.20.2+k3s1
k8scl3   Ready    <none>                 12d   v1.20.2+k3s1
k8scl2   Ready    control-plane,master   12d   v1.20.2+k3s1
k8scl4   Ready    <none>                 12d   v1.20.2+k3s1
root@k8scl1:~#
```

## Logging & Monitoring

InfluxDB, Grafana, Loki & Mail server installation

[Install VM](#install-VM)

[Install Influxdb](#Install-influxdb)

[Install Grafana](#Grafana-Installation)

[Install Loki](#Loki)

[Grafana Alerting](#Grafana-Alerting)

## Install VM

Its time to setup the monitoring, logging of the infrastructure. Here we are going to install and configure Loki , Influxdb, Grafana.

Create the new virtual machine in GCP demo-project project with centos 7 image and choose the disk size of 300GB. Virtual machine name should be `customername-monitoring`  (for example `customer-monitoring`, `colombia-monitoring`). Assign the static ip address to the vm

## Install influxdb

Install the repo and packages on newly created vm

```sh
cat <<EOF | sudo tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF
```

```sh
sudo yum -y install influxdb vim curl

sudo vim /etc/influxdb/influxdb.conf
[http]
auth-enabled = true

Then create a influxdb user with username as username an authentication password:

curl -XPOST "http://localhost:8086/query" --data-urlencode \
"q=CREATE USER username WITH PASSWORD 'strongpassword' WITH ALL PRIVILEGES"

sudo systemctl start influxdb && sudo systemctl enable influxdb
sudo systemctl start influxdb && systemctl enable influxdb
```

Login into influxdb with the username and password created above

```sh
influx -username 'username' -password 'password'

# create database using below command
create database metrics
```

## Grafana Installation

Grafana is the open source software to display the logs and metrics from the sources such as prometheus, influxdb, loki etc..

```sh
cat <<EOF | sudo tee /etc/yum.repos.d/grafana.repo
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF

sudo yum -y install grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

Default username and password for grafana is admin/admin

## Loki

Install Loki

Loki is the database to store the logs coming from the promtail agent running on each kubernetes node as daemonset. Promtail is pushing the logs to loki.

```sh
curl -s https://api.github.com/repos/grafana/loki/releases/latest | grep browser_download_url |  cut -d '"' -f 4 | grep loki-linux-amd64.zip | wget -i -

unzip loki-linux-amd64.zip
sudo mv loki-linux-amd64 /usr/local/bin/loki
loki --version
sudo mkdir -p /data/loki
sudo vim /etc/loki-local-config.yaml --> uploaded the file named as loki-local-config.yaml in the current repo under Infra-Set-K8s-Monitoring

Create Loki service

```sh
sudo tee /etc/systemd/system/loki.service<<EOF
[Unit]
Description=Loki service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/loki -config.file /etc/loki-local-config.yaml

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start loki.service
```

LogQL is query language to search the application/microservices logs in the grafana. These logs pushed by the promtail running on each kubernetes node. Here is the link of the website which can be used as reference for Loki search queries.

 <https://megamorf.gitlab.io/cheat-sheets/loki/>,

 <https://grafana.com/docs/loki/latest/logql/>

Screenshot showing Loki Query on grafana.

![Loki Query](Loki_query.PNG)

## Grafana Alerting

To send an alert from grafana we also need to setup postfix as mail server. Install the postfix package.

```sh
yum -y install postfix
```

Delete the default /etc/postfix/main.cf and add below content in the file. To allow other host to send email via this mail server add more ip addresses in mynetworks.

Use this website as a reference <https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-20-04>

```sh
queue_directory = /var/spool/postfix
command_directory = /usr/sbin
daemon_directory = /usr/libexec/postfix
data_directory = /var/lib/postfix
mail_owner = postfix
inet_interfaces = all
inet_protocols = all
mydestination = $myhostname, localhost.$mydomain, localhost
unknown_local_recipient_reject_code = 550
mynetworks = 127.0.0.0/8, 127.0.0.1/8 ### add more ip address if required 173.161.104.149/32
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
debug_peer_level = 2
debugger_command =
         PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
         ddd $daemon_directory/$process_name $process_id & sleep 5
sendmail_path = /usr/sbin/sendmail.postfix
newaliases_path = /usr/bin/newaliases.postfix
mailq_path = /usr/bin/mailq.postfix
setgid_group = postdrop
html_directory = no
manpage_directory = /usr/share/man
sample_directory = /usr/share/doc/postfix-2.11.2/samples
readme_directory = /usr/share/doc/postfix-2.11.2/README_FILES
relayhost = [smtp.sendgrid.net]:2525
smtp_tls_security_level = encrypt
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
header_size_limit = 4096000
smtp_sasl_security_options = noanonymous
smtp_generic_maps = hash:/etc/postfix/generic
canonical_maps = hash:/etc/postfix/canonical
```

Add below entry in generic, canonical file location under ``/etc/postfix` and after that run `postmap /etc/postfix/generic ; postmap /etc/postfix/canonical`

**Note:** Replace customer-monitoring with the name of the virtual machine

```sh
root@customer-monitoring.localdomain   demo@myapp.com
root@customer-monitoring.myapp.com customer-monitoring@myapp.com
```

Update the `/etc/hosts` file as mentioned below and here also repliace customer-monitoring with the name of the virtual machine

```sh
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 customer-monitoring.demo.cloud
11.242.0.125 customer-monitoring.demo.cloud
11.264.0.125 customer-monitoring.c.demo-project.internal customer-monitoring 
169.254.169.254 metadata.google.internal 
```

After the installation of loki, influxdb & grafana login into the grafana using default username & password admin/admin. Add the datasource from grafana dashboard for both influxdb, loki.

Here is the screenshot for the same.

### Add Datasources in grafana, click on wheel option highlighted in below screenshot

![Add influxdb & loki as datasource](grafana_datasource.PNG)

### Add InfluxDB as datasource in grafana

![Add influxdb as datasource](add_influxdb.PNG)

### Add Loki as datasource in grafana

![Add loki  as datasource](add_loki.PNG)

### Add New Dashboard

![Add loki  as datasource](add_dashboard.PNG)

### Datasource in query panel, refer to the influxb query <https://docs.influxdata.com/influxdb/cloud/query-data/flux/#query-fields-and-tags>

![Add datasource in query panel](datasource_query_panel.PNG)

## Telegraf Promtail Installation on K8s

To push server, database and rabbitmq metrics we need to install telegraf as a daemonset which will run on each kubernetes node and pushes metrics to influxdb database. Also we need to update telegraf's config so that it can push metrics to monitoring instance running influxdb. Similar update required for promtail agent (open source software to push logs to loki) and it will push logs instead of metrics to Loki.

In short, we are using InfluxDB to store metrics and Loki to store application logs.

Open the promtail-daemonset.yaml file and replace IP addr `x.x.x.x` with the static public ip address of monitoring virtual machine

```sh
- -client.url=http://xx.xx.xx.xx:3100/loki/api/v1/push
```

For telegraf open the file `telegraf-secrets.yaml` and replace the ip address

```sh
INFLUXDB_URL: http://xx.x.xx.xx:8086
```

Secondly, open the secret file telegraf/telegraf-config.yaml and update the password for rabbitmq user appuser.


```sh
    [[inputs.rabbitmq]]
        url = "http://rabbitmq.rabbitmq:15672"
        username = "appuser"
        password = "xxxxx" #### Set the password here
```

After changing the ip address for telegraf and promtail deploy the daemonset using command below command. Directory promail-daemonset,  telegraf-daemonset exist in this repo.

```sh
cd promail-daemonset
kubectl apply -f .
cd telegraf-daemonset
kubectl apply -f .
```

## Database Monitoring

Now time to setup monitoring and logging for database server. Because the database server is running on standalone machine and not part of kubernetes cluster, we need to install telegraf & promtail manually and configure it.

First install promtail agent:

```sh
curl -s https://api.github.com/repos/grafana/loki/releases/latest | grep browser_download_url |  cut -d '"' -f 4 | grep promtail-linux-amd64.zip | wget -i -
unzip promtail-linux-amd64.zip
sudo mv promtail-linux-amd64 /usr/local/bin/promtail

Open promtail config and add below content, replace ip address (xx.x.x.x.x) with vm public static ip address.

vim /etc/promtail-local-config.yaml
-------------------------------------
server:
  http_listen_port: 9080
  grpc_listen_port: 0
positions:
  filename: /var/log/positions.yaml
clients:
  - url: http://xx.xx.xx.xx:3100/loki/api/v1/push
scrape_configs:
- job_name: system
  static_configs:
  - targets:
      -  dbsrv1
    labels:
      job: dbsrv1_slow_query
      __path__: /var/log/postgresql/pg_slow_query.log
----------------------------------------
```

Create the service for promtail agent and below lines in the service file `/etc/systemd/system/promtail.service`.

```sh
[Unit]
Description=Promtail service
After=network.target
[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/promtail -config.file /etc/promtail-local-config.yaml
[Install]
WantedBy=multi-user.target
```

```sh
Start the agent service by running below commands

sudo systemctl start promtail.service
systemctl enable promtail.service
systemctl status promtail.service.
```

Install the telegraf agent:

```sh
apt install telegraf
```

Update the file /etc/telegraf/telegraf.conf as mentioned below and enter the correct password for postgres user & influxdb:

```sh
[[inputs.postgresql]]
  address = "host=localhost user=postgres password=password-for-postgres-user sslmode=disable"
[[outputs.influxdb]]
  retention_policy = ""
  write_consistency = "any"
  timeout = "5s"
  username = "username"
  password = "influxdb password we created during its installation"
[[inputs.cpu]]
    percpu = true
    totalcpu = true
    collect_cpu_time = false
    report_active = false
[[inputs.disk]]
    ignore_fs = ["tmpfs", "devtmpfs", "devfs"]
[[inputs.io]]
[[inputs.mem]]
[[inputs.net]]
[[inputs.system]]
[[inputs.swap]]
[[inputs.netstat]]
[[inputs.processes]]
[[inputs.kernel]]
```

## RabbitMQ Installation And Monitoring

We are using rabbitmq as statefulset in our microservices architecture and can be installed using below command.

**Note:** Install helm locally on your machine or master node


```sh
kubectl create ns rabbitmq

helm install rabbitmq --version 6.8.3 -n rabbitmq  --set rabbitmq.username=admin,rabbitmq.password=password --set replicas=3  --set image.tag=3.7.19 -f values.yaml  bitnami/rabbitmq
```

```sh
values.yaml:

podLabels:
   app: rabbitmq
affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - rabbitmq
            topologyKey: "kubernetes.io/hostname"
```

To see the rabbitmq pods are up and running run below command

```sh
root@k8scl1:~# kubectl get pods -n rabbitmq
NAME         READY   STATUS    RESTARTS   AGE
rabbitmq-0   1/1     Running   12         15d
rabbitmq-2   1/1     Running   1          2d13h
rabbitmq-1   1/1     Running   0          2d13h
root@k8scl1:~#
```

Port-forwarding to access the rabbitmq web ui

```sh
root@k8scl1:~# kubectl port-forward svc/rabbitmq -n rabbitmq 15672:15672
Forwarding from 127.0.0.1:15672 -> 15672
Forwarding from [::1]:15672 -> 15672
```

**Note:** Login to rabbitmq web UI and create user with the name appuser and set the password similar to one mentioned in the telegraf daemon set config file telegraf/telegraf-config.yaml

```sh
    [[inputs.rabbitmq]]
        url = "http://rabbitmq.rabbitmq:15672"
        username = "appuser"
        password = "xxxx"
```
