#!/usr/bin/python3
#
# Copyright (c) 2017 milisarge Mps Web Arayüzü için websocket aracı sunucusu
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from websocket_server import WebsocketServer
import os
import json
from mps import MpsIslev

kamusal_soket="https://localhost:16060/pub/mps?"
sertifika='/etc/nginx/ssl/mpsweb.crt'
bilgi_gonder='curl --cacert %s --request POST  -H "Accept: text/json" ' % sertifika
genel_kanal="genel_komut"
indirme_kanal="genel_komut_indirme"
iletim_betik="/opt/mpsweb/iletim.sh"

mps=MpsIslev()

def tr_cevir(mesaj):
	return mesaj.encode('iso-8859-1').decode('utf-8')

def genel_iletim(kanal,komut):
	os.system(iletim_betik+" "+kanal+" "+komut+" &")

def dosya_iletim(kanal,dosya):
	os.system(bilgi_gonder+kamusal_soket+'id='+kanal+' -d @'+dosya)

# Her elsıkışmadan(handshake) sonra çağrılacak yordam
def yeni_istemci(istemci, sunucu):
	print("Yeni istemci bağlandı ve verilen id: %d" % istemci['id'])
	sunucu.send_message_to_all("yeni istemci katıldı")

# İstemci bağlantıyı kestikten sonra çağrılacak yordam
def istemci_cikis(istemci, sunucu):
	print("İstemci(%d) ayrıldı" % istemci['id'])

# ws_araci / istemci
# İstemci bir mesaj gönderdiğinde çağrılacak yordam
def gelen_mesaj(istemci, sunucu, mesaj):
	if len(mesaj) > 200:
		mesaj = mesaj[:200]+'..'
	print("İstemci(%d) gönderdi: %s" % (istemci['id'], mesaj))
	mps_param=["@-kl","@kur","@odkp","@-dly"]
	if mesaj == "ping_dur":
		komut="killall -9 ping"
		genel_iletim(genel_kanal,komut)
	if mesaj == "ping":
		komut="ping 127.0.0.1"
		genel_iletim(genel_kanal,komut)
	if mesaj == "islem":
		os.system("./borulama "+indirme_kanal+" ./paketvt.sh")
		#os.system("./borulama ./paketvt.sh &")
	if "kamusal_mesaj=" in mesaj :
		icerik=mesaj.split("=")[1]
		sunucu.send_message_to_all(icerik)
	if any(x in mesaj for x in mps_param):
		genel_iletim(genel_kanal,mesaj)
	if "pkbilgi=" in mesaj :
		paket=mesaj.split("=")[1]
		mps.bilgi(paket)
		mps.kos()
		dosya_iletim("paket_bilgi","/tmp/mps_paket_bilgi_"+paket+".html")
	if "sistem_yukselt" in mesaj :
		genel_iletim(genel_kanal,mps.yukselt())
	if "pktalimat=" in mesaj :
		paket=mesaj.split("=")[1]
		genel_iletim(genel_kanal,mps.talimat(paket))
	if "pkkur=" in mesaj :
		paket=mesaj.split("=")[1]
		komut="mps kur "+paket+" --normal"
		genel_iletim(indirme_kanal,komut)
	if "pksil=" in mesaj :
		paket=mesaj.split("=")[1]
		komut="mps sil "+paket+" evet --normal"
		genel_iletim(genel_kanal,komut)
	if "pkkdl=" in mesaj :
		paket=mesaj.split("=")[1]
		komut="mps -kdl "+paket+" --normal"
		genel_iletim(genel_kanal,komut)
	if mesaj == "pkliste":
		os.system("mps paketler --json")
		dosya_iletim("paket_liste","/tmp/mps_paketler_listesi")
	if mesaj == "pkgrupliste":
		mps.gruplar()
		mps.kos()
		dosya_iletim("paket_grup_liste","/tmp/mps_paket_grup_listesi")
	if "grup_paketler=" in mesaj :
		grup=mesaj.split("=")[1]
		grup=tr_cevir(grup)
		mps.grup_paketler(grup)
		mps.kos()
		dosya_iletim("grup_paketler_liste","/tmp/mps_grup_paketler_listesi")
	if mesaj == "sistem":
		komut="./sistem_bilgi.sh"
		#genel_iletim(genel_kanal,komut)
		#os.system('curl --request POST  -H "Accept: text/json" http://127.0.0.1:36060 --data `./sistem_bilgi.sh`')
		sunucu.send_message(istemci,"sistem bilgisi gönderildi")
	if mesaj == "pingo":
		os.system("killall borulama")


PORT=36060
sunucu = WebsocketServer(PORT)
sunucu.set_fn_new_client(yeni_istemci)
sunucu.set_fn_client_left(istemci_cikis)
sunucu.set_fn_message_received(gelen_mesaj)
print ("%s portunda mps websocket aracı sunucusu çalışıyor" % PORT)
sunucu.run_forever()
