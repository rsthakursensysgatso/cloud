#
# Cookbook Name:: devops
# Recipe:: default
#
# Copyright 2016, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

#node["motd"]["author"].each  do | val |
  #output = echo "The value of author is #{val}"
#end

#if node["platform"] == ["centos"]
#  execute "yum -y install php" do#
    #command "yum -y install php"
    package "php" do
      action :install
    end
  #  end

  node["platform"] == ["centos"]
    package = node["centos"]["os"]
    #package "#{package}" do
      ## OR BELOW METHOD TO CALL THE ATTRIBUTE ##
   package node["centos"]["os"] do
      action :install
  end

if node["platform"] == ["centos"]
  #package "net-tools" do
  	execute "yum -y install net-tools" do
    action :install
end
end

node['var']['host'].each do |a, bc|
  n = "#{a}"
  directory  "/var/#{a}" do
  mode "0777"
  end
template "/var/test.rb" do
source "test.erb"
mode "0644"
variables(
  :name => bc["name"],
  :cast => bc["cast"]
 )
notifies :restart, "service[httpd]"
end
end

template "/etc/motd" do
      source "motd.rb"
      mode "600"
end

package "httpd" do
  action :install
end

template "/var/www/html/index.html" do
   source "apache.rb"
   mode "666"
end
service "httpd" do
  action :restart
end
service "httpd" do
  action [:enable, :start]
end

cookbook_file "/var/log/testing" do
  source "testing"
  mode "0644"
end

directory "/var/testdir/devops" do
  mode "0777"
  recursive true
end
