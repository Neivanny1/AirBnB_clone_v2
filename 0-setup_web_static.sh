#!/usr/bin/env bash
# Installs and prepares nginx server for static deployment


SERVER_CONFIG="server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;
    index index.html index.htm;
    error_page 404 /404.html;
    add_header X-Served-By \$hostname;

    location / {
        root /var/www/html/;
        try_files \$uri \$uri/ =404;
    }

    location /hbnb_static/ {
        alias /data/web_static/current/;
        try_files \$uri \$uri/ =404;
    }

    if (\$request_filename ~ redirect_me) {
        rewrite ^ https://sketchfab.com/bluepeno/models permanent;
    }

    location = /404.html {
        root /var/www/error/;
        internal;
    }
}"

HOME_PAGE="<!DOCTYPE html>
<html lang='en-US'>
    <head>
        <title>Home - Mombasa Tech Hub</title>
    </head>
    <body>
        <h1>Welcome To Tech Hub Mombasa</h1>
    </body>
</html>
"

# Check if Nginx is installed
if ! command -v nginx &> /dev/null; then
    apt-get update && apt-get -y install nginx
fi

# Create necessary directories
mkdir -p /var/www/html /var/www/error /data/web_static/releases/test /data/web_static/shared

# Set permissions
chmod -R 755 /var/www
chown -R ubuntu:ubuntu /data

# Create fake HTML file
echo -e "$HOME_PAGE" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
[ -e /data/web_static/current ] && rm -rf /data/web_static/current
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Update Nginx configuration
bash -c "echo -e '$SERVER_CONFIG' > /etc/nginx/sites-available/default"
ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'

# Restart Nginx
if [ "$(pgrep -c nginx)" -le 0 ]; then
    service nginx start
else
    service nginx restart
fi

