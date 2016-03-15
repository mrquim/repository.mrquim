from resources.lib.modules import client,webutils
import sys,os
from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'sportx'
        self.name = 'sports-x.net'
        self.icon = 'sportx.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False


class main():
	def __init__(self):
		self.base = 'http://www.sports-x.net/'

	def channels(self):
		html = client.request('http://www.sports-x.net/index.phplivetv', referer=self.base)
		channels = webutils.bs(html).find('article',{'class':'main'}).findAll('a')
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		urls=[]
		for channel in channels:
			url = channel['href']
			title = channel.getText()
			if url not in urls:
				urls.append(url)
				new.append((url,title,icon_path(info().icon)))
		#new.pop(-1)
		return new



	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)