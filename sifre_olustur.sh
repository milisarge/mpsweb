#!/bin/sh
if [ $1 ];then
	sudo sh -c "echo -n '$1:' >> /etc/nginx/.htpasswd"
	sudo sh -c "openssl passwd -apr1 >> /etc/nginx/.htpasswd"
else
	sudo cat /etc/shadow | grep `whoami` >> /etc/nginx/.htpasswd
fi
