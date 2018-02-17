#!/bin/bash


MY_POD_NAME=`hostname`
POD_IP=`ifconfig |grep 172|awk '{print $2}'`
val=$POD_IP


if [ "$MY_POD_NAME" = "consul-0" ];then
    echo "Consul-0"
    sed -i "s/IP/${val}/g" /etc/consul/consul0.json
    consul agent -server -config-dir /etc/consul/consul0.json

elif [ "$MY_POD_NAME" = "consul-1" ];then
    echo "Consul-1"
    sed -i "s/IP/${val}/g" /etc/consul/consul1.json
    consul agent -server -config-dir /etc/consul/consul1.json

elif [ "$MY_POD_NAME" = "consul-2" ];then
    echo "Consul-2"
    sed -i "s/IP/${val}/g" /etc/consul/consul2.json
    consul agent -server -config-dir /etc/consul/consul2.json
elif [ "$MY_POD_NAME" = "consul-3" ];then
    echo "Consul-3"
    sed -i "s/IP/${val}/g" /etc/consul/consul.json
    consul agent -server -config-dir /etc/consul/consul.json
fi
