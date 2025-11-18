FROM nginx:alpine

# Use our nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the web assets (player) into the default web root
COPY web/ /usr/share/nginx/html/
