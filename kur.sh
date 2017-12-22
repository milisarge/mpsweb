#!/bin/sh
if [ $1 ];then
	if [ -d $1 ];then
		_hedef=$1
		install -d $_hedef/etc/rc.d/init.d
		install -d $_hedef/usr/bin
		install -d $_hedef/etc/nginx/ssl
		install -d $_hedef/etc/nginx/conf.d
		install -d $_hedef/opt/mpsweb
		install -d $_hedef/srv/http/
		cp -rf http/mpsweb $_hedef/srv/http/
		cp -rf websocket_server *.sh $_hedef/opt/mpsweb/
		cp mpsweb.servis $_hedef/etc/rc.d/init.d/mpsweb
		[ -f mpsweb.crt ] && cp mpsweb.crt $_hedef/etc/nginx/ssl/mpsweb.crt
		[ -f mpsweb.key ] && cp mpsweb.key $_hedef/etc/nginx/ssl/mpsweb.key
		cp mpsweb-nginx.conf $_hedef/etc/nginx/conf.d/mpsweb
		ln -s /opt/mpsweb/sifre_olustur.sh $_hedef/usr/bin/mpsweb_sifre_olustur 
		ln -s /opt/mpsweb/sertifika_uret.sh $_hedef/usr/bin/mpsweb_sertifika_uret 
		ln -s /opt/mpsweb/ayarla.sh $_hedef/usr/bin/mpsweb_ayarla 
	else
		echo "hedef dizin yolu tanımsız!"
	fi
else
	echo "kurulacak hedef dizin belirtiniz!"
fi
