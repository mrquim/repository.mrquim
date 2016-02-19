from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,sys,xbmcgui,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'time4tv'
        self.name = 'Time4tv.com'
        self.icon = 'time4tv.jpg'
        self.paginated = False
        self.categorized = True
        self.multilink = True
class main():
	def __init__(self,url = 'http://castalba.tv/channels'):
		self.base = 'http://www.time4tv.com/'
		self.url = url

	def links(self,url):
		try:
			html = client.request(url)
			url = re.findall('(http://tv4embed.com/[^"\']+)',html)[0]
			html = client.request(url)
			hm = re.findall('<a(.+)\s*<iframe',html)[0]
			links = re.findall('href=(?:"|\')(.+?)(?:"|\')',hm)
			links = self.__prepare_links(links)
			return links
		except:
			return []

	def categories(self):
		out = [('http://www.time4tv.com/categories/sports-channels.php','Sport channels', icon_path(info().icon)),('http://www.time4tv.com/categories/usa-channels.php','USA Channels', icon_path(info().icon)),
				('http://www.time4tv.com/categories/uk-channels.php','UK Channels', icon_path(info().icon))]
		return out

	def channels(self,url):
		self.url = url
		html = client.request(url, referer=self.base)
		soup = webutils.bs(html)
		channels = soup.find('div',{'class':'categoryChannels'}).findAll('li')
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = channel.find('a')['href']
			img = channel.find('img')['src'].replace('../',self.base)
			title = channel.getText()
			new.append((url,title,img))
		return new

	def __prepare_links(self,links):
		new=[]
		i = 1
		for channel in links:
			url = channel
			title = 'Link %s'%i
			new.append((url,title))
			i+=1
		return new



