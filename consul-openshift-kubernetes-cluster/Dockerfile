FROM docker.io/centos
#RUN YOURIP = ifconfig |grep 172|awk '{print $2}'
RUN yum -y install epel-release && yum -y install unzip wget net-tools bind-utils
RUN cd /tmp && wget https://releases.hashicorp.com/consul/1.0.3/consul_1.0.3_linux_amd64.zip?_ga=2.256698818.878308909.1517575526-1194691973.1517340593
RUN cd /tmp && unzip consul_1*
RUN chmod +x /tmp/consul && cp /tmp/consul /usr/bin && cp /tmp/consul  /usr/sbin
RUN mkdir -p /etc/consul 
RUN mkdir -p /opt/consul
COPY consul.json /etc/consul/
COPY consul0.json /etc/consul/
COPY consul1.json /etc/consul/
COPY consul2.json /etc/consul/
COPY web.json /etc/consul/
COPY start.sh /var/
RUN chmod 777 -R /etc/consul
RUN chmod 777 -R /opt/consul
RUN chmod +x /var/start.sh
EXPOSE 8500 8300 8400 8301 8302 8600 53 
CMD ["/var/start.sh"]
#CMD ["consul", "agent", "-server", "-config-dir", "/etc/consul"]
#RUN  consul agent -server -config-dir /etc/consul
#CMD ["consul agent -server -bootstrap-expect 1 \
#    -data-dir /tmp/consul -node=agent-one \
#    -bind=$YOURIP \
#    -client=0.0.0.0 \
#    -config-dir /etc/consul.d \
#    -ui-dir /opt/consul-ui"]
#EXPOSE 8500 8300 8400 8301 8302
#CMD ["/bin/bash",  "/var/init.sh"]
#CMD ["/var/init.sh"]
