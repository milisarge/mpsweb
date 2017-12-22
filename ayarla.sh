#!/bin/sh
# websocket iletişimi için nginx nchan modülünün genel ayarlara eklenmesi
sudo sed -i '1s/^/load_module \/usr\/lib\/nginx\/modules\/ngx_nchan_module.so; \n /'  /etc/nginx/nginx.conf
# mpsweb nginx ayarlarının nginx ayar dizinine kopyalanıp genel ayarlara eklenmesi
sudo sed -i '/include       mime.types;/ a\    include conf.d/mpsweb;' /etc/nginx/nginx.conf
