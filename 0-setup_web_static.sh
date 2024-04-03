#!/usr/bin/env bash
# Script that sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership of /data folder recursively to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i '/^\s*location \/hbnb_static/ { 
    /^\s*location \/hbnb_static/!b
    n
    c\ \ \ \ alias /data/web_static/current/; 
}' "$config_file"

# Restart Nginx
sudo service nginx restart

exit 0
