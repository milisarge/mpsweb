#!/bin/sh
if [ $1 ];then
	sh -c "echo -n '$1:' >> /etc/nginx/.htpasswd"
	sh -c "openssl passwd -apr1 >> /etc/nginx/.htpasswd"
else
	cat /etc/shadow | grep `whoami` >> /etc/nginx/.htpasswd
fi
