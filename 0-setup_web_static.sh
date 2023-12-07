#!/usr/bin/env bash
# prepares nginx server for static deployment
sudo apt update
sudo apt install nginx -y

# make required folders
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared/
echo "<h1>Welcome to tech coders</h1>" | sudo dd status=none of=/data/web_static/releases/test/index.html
# creates symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown _R ubuntu:ubuntu /data/

#settting backup for config files
sudo cp /etc/nginx/sites-enabled/default nginx-sites-enabled_default.backup
# setting contents for redirect
sudo sed -i '37i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
# restarts the server
sudo service nginx restart
