#!/usr/bin/bash
#cd /var/heroku
#git clone https://github.com/heroku/ruby-rails-sample
#chmod 777 /var/heroku
#git clone https://github.com/heroku/ruby-rails-sample
gem install bundler
gem install pg -- --with-pg-config=/usr/bin/pg_config
gem install nokogiri -v '1.6.6.2'
gem install puma -v '2.11.1'
gem install pg -v '0.18.1'
bundle install
git clone https://github.com/Linuxbrew/brew.git ~/.linuxbrew
PATH="$HOME/.linuxbrew/bin:$PATH"
echo 'export PATH="$HOME/.linuxbrew/bin:$PATH"' >>~/.bash_profile
export PATH="$HOME/.linuxbrew/bin:$PATH"
export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
cd /var/heroku/;/usr/local/bin/bundle exec rake bootstrap;brew install heroku;heroku local &
