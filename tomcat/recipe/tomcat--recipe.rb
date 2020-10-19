package "tomcat" do
action :install
only_if { node.default['platform'] = 'CentOS'}
end

service "tomcat" do
  action :restart
end
service "tomcat" do
  action [:enable, :start]
end

node['tomcat']['host'].each do |a, bc|
  n = "#{a}"
directory  "/var/#{a}" do
file  "/usr/share/tomcat/conf/#{a}-users.xml" do
mode "0777"
end
template "/usr/share/tomcat/conf/tomcat-users.xml" do
     source "tomcat.xml"
      mode "0644"
      variables(
      :username => bc["username"],
      :password => bc["redhat"]
        )
notifies :restart, "service[tomcat]"
   end
      end
 #
