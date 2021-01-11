sudo apt update
apt-cache policy docker-ce
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt-get update
sudo apt update
sudo apt install docker.io docker-compose nginx openssl unzip -y
sudo systemctl start docker && sudo systemctl enable docker
sudo mkdir /etc/ssl/cert
sudo chmod +x /tmp/files/gen-cer.sh && /tmp/files/gen-cer.sh sentry-arachnys-task 
sudo cp -f sentry-arachnys-task.crt /etc/ssl/cert 
sudo cp -f sentry-arachnys-task.key /etc/ssl/cert
sudo cp -f /tmp/files/sentry.arachnys-task.conf /etc/nginx/conf.d/
sudo wget https://github.com/getsentry/onpremise/archive/20.12.1.zip
sudo unzip 20.12.1.zip
cd /home/ubuntu/onpremise-20.12.1 
#&& sudo rm -f install.sh
#sudo cp -f /tmp/files/install.sh /home/ubuntu/onpremise-20.12.1
#sudo cp -f /tmp/files/docker-compose.yml /home/ubuntu/onpremise-20.12.1
#sudo chmod +x install.sh
sudo ./install.sh  --no-user-prompt
sudo docker-compose up -d
sudo systemctl restart nginx && sudo systemctl enable nginx
