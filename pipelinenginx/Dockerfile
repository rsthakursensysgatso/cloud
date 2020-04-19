FROM ubuntu:16.04

MAINTAINER Ravinder

RUN apt-get update \
    && apt-get install -y nginx  ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*  /etc/nginx/nginx.conf
    #&& echo "daemon off;" >> /etc/nginx/nginx.conf

ADD https://get.aquasec.com/microscanner .
RUN chmod +x microscanner
RUN ./microscanner OGY0NGQ3MTI3NmQ4

EXPOSE 80
CMD ["nginx", "-c", "/usr/share/nginx/nginx.conf"]
