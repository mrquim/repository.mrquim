from __future__ import unicode_literals
from resources.lib.modules import client,convert,webutils
from resources.lib.modules.log_utils import log

import re,sys
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

class info():
    def __init__(self):
    	self.mode = 'iptvlinks'
        self.name = 'iptvlinks.eu'
        self.icon = 'iptvlinks.png'
        self.categorized = False
        self.paginated = True
        self.multilink = True

class main():
	def __init__(self, url='http://www.iptvlinks.eu/'):
		self.base = 'http://www.iptvlinks.eu/'
		self.url = url

	def events(self):
		html = client.request(self.url, referer=self.base)
		html = convert.unescape(html.decode('utf-8'))
		events = webutils.bs(html).findAll('h1', {'class':'entry-title'})
		events = self.__prepare_events(events)
		return events

	
	
	def __prepare_events(self,events):
		new = []
		for event in events:
			url = event.find('a')['href']
			title = event.getText().replace('IPTV Channels & Streaming','')
			if 'playlist' not in title.lower():
				new.append((url,title.encode('utf-8', 'xmlcharrefreplace')))
		return new

	def links(self,url):
		log(url)
		html=client.request(url)
		try:	ace = self.prepare_ace(html)
		except:	ace = []
		try:	iptv = self.prepare_iptv(re.findall('href="(.+?)">(?:<strong>)?\s*(.+?\s*IPTV) Link<',html))
		except:	iptv = []
		try:	flash = self.prepare_flash(re.findall('(Flash Stream.+?):\s*<a href="(.+?)">',html))
		except:	flash = []
		urls = ace+iptv+flash
		return urls

	def prepare_ace(self,html):
		new=[]
		links = webutils.bs(html).find('pre').getText().split('\n')
		for link in links:
			if 'acestream' in link or 'bit.ly' in link:
				url = link
				new.append((url,title))
			else:
				title = link + ' Acestream'
				

			
		return new

	def prepare_flash(self,links):
		new=[]
		for link in links:
			url = link[1]
			title = link[0]
			new.append((url,title))
			
		return new

	def prepare_iptv(self,links):
		new=[]
		for link in links:
			title = link[1]
			url = self.rslv(link[0])
			new.append((url,title))
		return new

	def rslv(self,url):
		html = client.request(url)
		url = re.findall('(https?:.+?\.ts)',html)[0]
		return url

	def next_page(self):
		try:
			html = client.request(self.url)
			next = re.findall('rel=[\'\"]next[\'\"].+?href=[\'\"](.+?)[\'\"]',html)[0]
			return next
		except:
			return None

	def resolve(self,url):
		if url.endswith('.ts') or 'bit.ly' in url:
			return url
		else:
			import liveresolver
			return liveresolver.resolve(url)