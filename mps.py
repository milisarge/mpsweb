#!/usr/bin/python3
#
# Copyright (c) 2017 milisarge MPS İşlev (Api) Sınıfı
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

import os
import subprocess

class MpsIslev():
	
	aktif_komut=[]
	
	def kos(self,komut="@aktif_komut",donus=False):
		cikti=""
		if komut == "@aktif_komut":
			#os.system(self.aktif_komut)
			cikti = subprocess.check_output(self.aktif_komut)
		else:
			#os.system(komut)
			cikti = subprocess.check_output(komut)
		#print (self.tr_cevir(cikti))
		if donus:
			return self.tr_cevir(cikti)
	
	def surum(self):
		self.aktif_komut=["mps","-v"]
		return self.aktif_komut
		
	def talimat(self,paket):
		self.aktif_komut=["mps","talimat",paket]
		komut="%s %s %s" % ("mps","talimat",paket)
		return komut
	
	def gruplar(self,cikti="--json"):
		self.aktif_komut=["mps","gruplar",cikti]
		komut="%s %s %s" % ("mps","gruplar",cikti)
		return komut
	
	def grup_paketler(self,grup,cikti="--json"):
		self.aktif_komut=["mps","paketler",grup,cikti]
		komut="%s %s %s %s" % ("mps","paketler",grup,cikti)
		return komut
	
	def bilgi(self,paket,renk="yok"):
		if renk=="yok":
			renkdurum="--html"
		self.aktif_komut=["mps","-b",paket,renkdurum]
		return self.aktif_komut
		
	def tr_cevir(self,cikti):
		return cikti.decode('utf-8')

# test
'''
mps=MpsIslev()
print(mps.talimat("atool"))
mps.kos()
'''
