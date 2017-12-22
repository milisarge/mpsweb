#!/bin/sh
# gelen komutun pipe yardımıyla çıktısının ilgili websokete satır satır iletilmesi

_adres='https://localhost:16060/pub/mps?id='
_kanal='genel_komut'
_iletim_tip='-H Accept: text/json'
_sertifika='--cacert /etc/nginx/ssl/mpsweb.crt'

[ "$1" ] && _kanal="$1" || exit 1;

PIPE=$(mktemp -u)

[[ ! -p $PIPE ]] && mkfifo -m 600 $PIPE || exit 1;

shift
$@ > $PIPE &

echo "tip: $_kanal $@ komutu işletiliyor"

while read -r satir;do
   curl $_sertifika --request POST  "$_iletim_tip" $_adres$_kanal --data "$satir"
done < $PIPE

rm $PIPE
