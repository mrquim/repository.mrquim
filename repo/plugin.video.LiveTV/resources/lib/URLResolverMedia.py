#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2015 xsteal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json, re, xbmc, urllib, xbmcgui, os, sys, pprint, urlparse, urllib2
from t0mm0.common.net import Net
from bs4 import BeautifulSoup
import jsunpacker
import AADecoder

class GoogleVideo():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}


	def getId(self):
		return urlparse.urlparse(self.url).path.split("/")[-2]

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.url, headers=self.headers).content.decode('unicode_escape')
		formatos = {
		'5': {'ext': 'flv'},
		'6': {'ext': 'flv'},
		'13': {'ext': '3gp'},
		'17': {'ext': '3gp'},
		'18': {'ext': 'mp4'},
		'22': {'ext': 'mp4'},
		'34': {'ext': 'flv'},
		'35': {'ext': 'flv'},
		'36': {'ext': '3gp'},
		'37': {'ext': 'mp4'},
		'38': {'ext': 'mp4'},
		'43': {'ext': 'webm'},
		'44': {'ext': 'webm'},
		'45': {'ext': 'webm'},
		'46': {'ext': 'webm'},
		'59': {'ext': 'mp4'}
		}
		formatosLista = re.search(r'"fmt_list"\s*,\s*"([^"]+)', sourceCode).group(1)
		formatosLista = formatosLista.split(',')
		streamsLista = re.search(r'"fmt_stream_map"\s*,\s*"([^"]+)', sourceCode).group(1)
		streamsLista = streamsLista.split(',')

		videos = []
		qualidades = []
		i = 0
		for stream in streamsLista:
			formatoId, streamUrl = stream.split('|')
			form = formatos.get(formatoId)
			extensao = form['ext']
			resolucao = formatosLista[i].split('/')[1]
			largura, altura = resolucao.split('x')
			if 'mp' in extensao or 'flv' in extensao:
				qualidades.append(altura+'p '+extensao)
				videos.append(streamUrl)
			i+=1
		qualidade = xbmcgui.Dialog().select('Escolha a qualidade', qualidades)
		return videos[qualidade]


class UpToStream():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}

	def getId(self):
		return re.compile('http\:\/\/uptostream\.com\/(.+)').findall(self.url)[0]

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.url, headers=self.headers).content

		links = re.compile('source\s+src=[\'\"]([^\'\"]+)[\'\"].+?data-res=[\'\"]([^\"\']+)[\'\"]').findall(sourceCode)
		videos = []
		qualidades = []
		for link, qualidade in links:
			if link.startswith('//'):
				link = "http:"+link
			videos.append(link)
			qualidades.append(qualidade)
		videos.reverse()
		qualidades.reverse()
		qualidade = xbmcgui.Dialog().select('Escolha a qualidade', qualidades)
		return videos[qualidade]

class OpenLoad():

	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.id = str(self.getId())
		self.messageOk = xbmcgui.Dialog().ok
		self.site = 'https://openload.co'
		#self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

	def getId(self):
		#return self.url.split('/')[-1]
		try:
			return re.compile('https\:\/\/openload\.co\/embed\/(.+?)\/').findall(self.url)[0]
		except:
			return re.compile('https\:\/\/openload.co\/f\/(.+?)\/').findall(self.url)[0]


	def base10toN(self,num,n):
		num_rep = {10: 'a',
		11: 'b',
		12: 'c',
		13: 'd',
		14: 'e',
		15: 'f',
		16: 'g',
		17: 'h',
		18: 'i',
		19: 'j',
		20: 'k',
		21: 'l',
		22: 'm',
		23: 'n',
		24: 'o',
		25: 'p',
		26: 'q',
		27: 'r',
		28: 's',
		29: 't',
		30: 'u',
		31: 'v',
		32: 'w',
		33: 'x',
		34: 'y',
		35: 'z'}
		new_num_string = ''
		current = num
		while current != 0:
			remainder = current % n
			if 36 > remainder > 9:
				remainder_string = num_rep[remainder]
			elif remainder >= 36:
				remainder_string = '(' + str(remainder) + ')'
			else:
				remainder_string = str(remainder)
			new_num_string = remainder_string + new_num_string
			current = current / n

		return new_num_string


	def decodeOpenLoad(self, aastring):
	    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]+(oﾟｰﾟo)+ ((c^_^o)-(c^_^o))+ (-~0)+ (ﾟДﾟ) ['c']+ (-~-~1)+","")
	    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
	    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))","8")
	    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))","7")
	    aastring = aastring.replace("((o^_^o) +(o^_^o))","6")
	    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))","5")
	    aastring = aastring.replace("(ﾟｰﾟ)","4")
	    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))","2")
	    aastring = aastring.replace("(o^_^o)","3")
	    aastring = aastring.replace("(ﾟΘﾟ)","1")
	    aastring = aastring.replace("(+!+[])","1")
	    aastring = aastring.replace("(c^_^o)","0")
	    aastring = aastring.replace("(0+0)","0")
	    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]","\\")
	    aastring = aastring.replace("(3 +3 +0)","6")
	    aastring = aastring.replace("(3 - 1 +0)","2")
	    aastring = aastring.replace("(!+[]+!+[])","2")
	    aastring = aastring.replace("(-~-~2)","4")
	    aastring = aastring.replace("(-~-~1)","3")
	    aastring = aastring.replace("(-~0)","1")
	    aastring = aastring.replace("(-~1)","2")
	    aastring = aastring.replace("(-~3)","4")
	    aastring = aastring.replace("(0-0)","0")

	    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
	    decodestring = "\\+"+ decodestring
	    decodestring = decodestring.replace("+","")
	    decodestring = decodestring.replace(" ","")

	    decodestring = self.decode(decodestring)
	    decodestring = decodestring.replace("\\/","/")

	    if 'toString' in decodestring:
	        base = re.compile(r"toString\(a\+(\d+)", re.DOTALL | re.IGNORECASE).findall(decodestring)[0]
	        base = int(base)
	        match = re.compile(r"(\(\d[^)]+\))", re.DOTALL | re.IGNORECASE).findall(decodestring)
	        for repl in match:
	            match1 = re.compile(r"(\d+),(\d+)", re.DOTALL | re.IGNORECASE).findall(repl)
	            base2 = base + int(match1[0][0])
	            repl2 = self.base10toN(int(match1[0][1]),base2)
	            decodestring = decodestring.replace(repl,repl2)
	        decodestring = decodestring.replace("+","")
	        decodestring = decodestring.replace("\"","")
	        videourl = re.search(r"(http[^\}]+)", decodestring, re.DOTALL | re.IGNORECASE).group(1)
	        videourl = videourl.replace("https","http")
	    else:
	        return decodestring

	    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
	    headers = {'User-Agent': UA }

	    req = urllib2.Request(videourl,None,headers)
	    res = urllib2.urlopen(req)
	    videourl = res.geturl()


	    return videourl



	def decode(self, encoded):
	    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
	        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
	    return encoded.decode('utf8')

	def getMediaUrl(self):

		#content = self.net.http_GET(self.url, headers=self.headers).content

		#videoUrl = self.decodeOpenLoad(str(content.encode('utf-8')))

		headers1 = {
		        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		       'Accept-Encoding': 'none',
		       'Accept-Language': 'en-US,en;q=0.8',
		       'Connection': 'keep-alive'
		    }

		req = urllib2.Request(self.url, headers=headers1)
		response = urllib2.urlopen(req)
		sHtmlContent = response.read()
		response.close()

		aastring = re.compile("<script[^>]+>(ﾟωﾟﾉ[^<]+)<", re.DOTALL | re.IGNORECASE).findall(sHtmlContent)
		hahadec = self.decodeOpenLoad(aastring[0])
		haha = re.compile(r"welikekodi_ya_rly = Math.round([^;]+);", re.DOTALL | re.IGNORECASE).findall(hahadec)[0]
		haha = eval("int" + haha)

		videoUrl = self.decodeOpenLoad(aastring[haha])


		#print videoUrl

		return videoUrl

	def getDownloadUrl(self):
		content = self.net.http_GET(self.url, headers=self.headers).content

		url = self.decodeOpenLoad(str(content.encode('utf-8')))

		return url

	def getMediaUrlOld(self):

		try:
			ticket = 'https://api.openload.co/1/file/dlticket?file=%s' % self.id
			result = self.net.http_GET(ticket).content
			jsonResult = json.loads(result)

			if jsonResult['status'] == 200:
				fileUrl = 'https://api.openload.co/1/file/dl?file=%s&ticket=%s' % (self.id, jsonResult['result']['ticket'])
				captcha = jsonResult['result']['captcha_url']

				print "CAPTCHA: "
				print self.id
				captcha.replace('\/', '/')
				print captcha

				if captcha:
					captchaResponse = self.getCaptcha(captcha.replace('\/', '/'))

					if captchaResponse:
						fileUrl += '&captcha_response=%s' % urllib.quote(captchaResponse)

				xbmc.sleep(jsonResult['result']['wait_time'] * 1000)

				result = self.net.http_GET(fileUrl).content
				jsonResult = json.loads(result)

				if jsonResult['status'] == 200:
					return jsonResult['result']['url'] + '?mime=true'  #really?? :facepalm:
				else:
					self.messageOk('Live!t-TV', "FILE: "+jsonResult['msg'])

			else:

				self.messageOk('Live!t-TV', "TICKET: "+jsonResult['msg'])
				return False
		except:
			self.messageOk('Live!t-TV', 'Ocorreu um erro a obter o link. Escolha outro servidor.')

	def getCaptcha(self, image):
		try:
			image = xbmcgui.ControlImage(450, 0, 300, 130, image)
			dialog = xbmcgui.WindowDialog()
			dialog.addControl(image)
			dialog.show()
			xbmc.sleep(3000)

			letters = xbmc.Keyboard('', 'Escreva as letras na imagem', False)
			letters.doModal()

			if(letters.isConfirmed()):
				result = letters.getText()
				if result == '':
					self.messageOk('Live!t-TV', 'Tens de colocar o texto da imagem para aceder ao video.')
				else:
					return result
			else:
				self.messageOk('Live!t-TV', 'Erro no Captcha')
		finally:
			dialog.close()

	def getSubtitle(self):
		pageOpenLoad = self.net.http_GET(self.url, headers=self.headers).content

		try:
			subtitle = re.compile('<track\s+kind="captions"\s+src="(.+?)"').findall(pageOpenLoad)[0]
		except:
			subtitle = ''
		#return self.site + subtitle
		return subtitle


class VideoMega():

	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.id = str(self.getId())
		self.messageOk = xbmcgui.Dialog().ok
		self.site = 'https://videomega.tv'
		self.headers = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
		self.headersComplete = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25', 'Referer': self.getNewHost()}

	def getId(self):
		return re.compile('http\:\/\/videomega\.tv\/view\.php\?ref=(.+?)&width=700&height=430').findall(self.url)[0]

	def getNewHost(self):
		return 'http://videomega.tv/cdn.php?ref=%s' % (self.id)

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.getNewHost(), headers=self.headersComplete).content
		match = re.search('<source\s+src="([^"]+)"', sourceCode)

		if match:
			return match.group(1) + '|User-Agent=%s' % (self.headers)
		else:
			self.messageOk('Live!t-TV', 'Video nao encontrado.')

class Vidzi():
	def __init__(self, url):
		self.url = url
		self.net = Net()
		self.id = str(self.getId())
		self.messageOk = xbmcgui.Dialog().ok
		self.site = 'https://videomega.tv'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
		self.subtitle = ''

	def getId(self):
		return re.compile('http\:\/\/vidzi.tv\/embed-(.+?)-').findall(self.url)[0]

	def getNewHost(self):
		return 'http://vidzi.tv/embed-%s.html' % (self.id)

	def getMediaUrl(self):
		sourceCode = self.net.http_GET(self.getNewHost(), headers=self.headers).content

		if '404 Not Found' in sourceCode:
			self.messageOk('Live!t-TV', 'Ficheiro nao encontrado ou removido. Escolha outro servidor.')

		match = re.search('file\s*:\s*"([^"]+)', sourceCode)
		if match:
			return match.group(1) + '|Referer=http://vidzi.tv/nplayer/jwpayer.flash.swf'
		else:
			for pack in re.finditer('(eval\(function.*?)</script>', sourceCode, re.DOTALL):
				dataJs = jsunpacker.unpack(pack.group(1)) # Unpacker for Dean Edward's p.a.c.k.e.r | THKS

				#print dataJs
				#pprint.pprint(dataJs)

				stream = re.search('file\s*:\s*"([^"]+)', dataJs)
				try:
					subtitle = re.compile('tracks:\[\{file:"(.+?)\.srt"').findall(dataJs)[0]
					subtitle += ".srt"
				except:
					subtitle = re.compile('tracks:\[\{file:"(.+?)\.vtt"').findall(dataJs)[0]
					subtitle += ".vtt"
				self.subtitle = subtitle

				if stream:
					return stream.group(1)

		self.messageOk('Live!t-TV', 'Video nao encontrado. Escolha outro servidor')


	def getSubtitle(self):
		return self.subtitle
