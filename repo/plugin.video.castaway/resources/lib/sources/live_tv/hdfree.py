from __future__ import unicode_literals
from resources.lib.modules import client
import re


class info():
    def __init__(self):
    	self.mode = 'hdfree'
        self.name = 'HDFree.tv'
        self.icon = 'hdfree.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self):
		self.base = 'http://hdfree.tv/tvlogos.html'

	def channels(self):
		html = client.request(self.base, referer=self.base)
		regex='<a href="(.+?)".+?><img src="(.+?)" .+?></a>'
		reg=re.compile(regex)
		channels = re.findall(regex,html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		channels.pop(0)
		for channel in channels:

			img = 'http://hdfree.tv' + channel[1]
			url = channel[0]
			title = re.findall('(?:.tv|\d+)/(.+?)-live',url)[0].replace('-',' ').title().replace('Watch', '').lstrip("0123456789=/,")
			new.append((url,title,img))
		return new



