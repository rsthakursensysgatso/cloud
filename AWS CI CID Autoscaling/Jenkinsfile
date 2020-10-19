node {
   
   	stage 'Stage 1'
   		echo 'Hello Deploying Docker App'
   	stage 'Checkout'
   		git url: 'https://github.com/rsthakur83/challenge'
   
      stage 'Execute'
         sh 'chmod +x docker.sh'
      stage 'Deploy in Test Env'
         sh './docker.sh'
 
      stage 'Deploy to Prod approval'
        input "Deploy to prod?"

      stage 'app release'
         sh 'echo release'
      stage 'Supply app version'
         sh 'chmod +x release;./release'
      stage 'Web Directory'
         sh  'echo "sudo cp -rf release/* /usr/share/httpd/noindex" >> userdata.sh'
         sh  'echo "sudo cp -rf release/* /var/www/html" >> userdata.sh'

 
      stage 'Changing Env'
         sh 'chmod +x scaling.sh'
      stage 'Swaping Blue with Green'
         sh './scaling.sh'
   
 }
