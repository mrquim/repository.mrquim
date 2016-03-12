from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,urlparse,urllib,sys,os

from addon.common.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'nbafull'
        self.name = 'nbafull.com (full replays)'
        self.icon = 'nbafull.png'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://nbafull.com'):
		self.base = 'http://nbafull.com'
		self.url = url

	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items=soup.findAll('div',{'class':'thumb'})
		out=[]
		for item in items:
			url = item.find('a')['href']
			title=item.find('a')['title'].encode('utf-8')
			title = re.sub('<[^>]*>','',title)
			out+=[[title,url,icon_path(info().icon)]]

		return out

	def links(self,url, img=' '):
		if 'nbafull.com' not in url:
			url = self.base + url

		out = []
		html = client.request(url)
		soup = webutils.bs(html)
		videos = soup.findAll('video')
		for video in videos:
			url = video.find('source')['src']
			title = video.findPrevious('p').getText()
			out.append((title,url,icon_path(info().icon)))


		return out





	def resolve(self,url):
		return url




	def next_page(self):

		html = client.request(self.url)
		try:
			next_page=re.findall('<a.+?rel="next".+?href="(.+?)"',html)[0]
			if 'nbafull.com' not in next_page:
				next_page = self.base + next_page
		except:
			next_page=None
		return next_page


