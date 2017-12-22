#!/bin/sh
mkdir -p /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/mpsweb.key -out /etc/nginx/ssl/mpsweb.crt
#openssl x509 -in /etc/nginx/ssl/mpsweb.crt -out /etc/ssl/certs/mpsweb.pem -outform PEM
