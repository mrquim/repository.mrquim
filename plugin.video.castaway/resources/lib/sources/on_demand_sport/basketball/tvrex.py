from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,urlparse,sys
from addon.common.addon import Addon

addon = Addon('plugin.video.castaway', sys.argv)


class info():
    def __init__(self):
    	self.mode = 'tvrex'
        self.name = 'tvrex.net (full replays)'
        self.icon = 'tvrex.jpg'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://tvrex.net/'):
		self.base = 'http://tvrex.net/'
		self.url = url

	def items(self):
		html = client.request(self.url)
		items = re.findall('<div class="post-img">\s*<a href="(.+?)">\s*<img.+?data-hidpi="(.+?)" alt="(.+?)"',html)
		out=[]
		for item in items:
			url = item[0]
			title=item[2]
			thumb=item[1]

			out+=[[title,url,thumb]]
		out.pop(0)
		return out

	def links(self,url, img=' '):
		if self.base not in url:
			url = self.base + url
		html = client.request(url).decode('utf-8')
		html = html.replace('<SCRIPT data-cfasync="false" SRC="//bdv.bidvertiser.com/BidVertiser.dbm?pid=663980&bid=1759686" TYPE="text/javascript"></SCRIPT>','')
		out = []
		links = re.findall('>(.+?)<.+?\s*<iframe.+?src=[\"\'](.+?)[\"\']',html)
		for link in links:
			title = link[0]
			url = link[1]
			out.append((title,url,img))

		


		links = re.findall('<source src=[\"\']([^"]+)[\"\'] type=[\"\']video/mp4[\"\'] data-res=[\"\']720p[\"\']',html)
		found = 0
		i=0
		for link in links:
			i+=1
			title1 ='Part %s'%i 
			url1 = link
			out.append((title1,url1,img))
			found=1

		if not found:
			i=0
			links = re.findall('<source src=[\"\']([^"]+)[\"\'] type=[\"\']video/mp4[\"\'] data-res=[\"\']360p[\"\']',html)
			for link in links:
				i+=1
				title1 ='Part %s'%i
				url1 = link
				out.append((title1,url1,img))


		return out





	def resolve(self,url):
		import urlresolver
		return urlresolver.resolve(url)




	def next_page(self):
		html = client.request(self.url)
		try:
			next_page=re.findall("class='current'>.+?</span><a href=\'(.+?)\'",html)[0]
		except:
			next_page=None
		return next_page


