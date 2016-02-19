from __future__ import unicode_literals
from resources.lib.modules import client
import re, urllib


class info():
    def __init__(self):
    	self.mode = 'serbiaplus'
        self.name = 'serbiaplus.com'
        self.icon = 'serbiaplus.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self,url = 'http://www.serbiaplus.com/menu2.html'):
		self.base = 'http://www.serbiaplus.com/'
		self.url = url

	

	def channels(self):
		html = client.request(self.url, referer=self.base)
		channels=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?/(.+?).(?:jpg|png|gif))" width=".+?" height=".+?"').findall(html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = self.base + channel[0]
			img = self.base + urllib.quote(channel[1])
			title = channel[2].title()
			new.append((url,title,img))
		return new

	


